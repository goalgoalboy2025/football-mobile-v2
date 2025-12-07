import flet as ft
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import re
import json
import concurrent.futures

# --- Configuration & Data ---

TEAMS = {
    "Arsenal": "arsenal",
    "Man City": "manchester-city",
    "Liverpool": "liverpool",
    "Chelsea": "chelsea",
    "Real Madrid": "real-madrid",
    "Barcelona": "barcelona",
    "Atletico Madrid": "atletico-madrid",
    "Bayern Munich": "bayern-munich",
    "PSG": "paris-saint-germain",
    "China": "china",
    "Germany": "germany",
    "France": "france",
    "Spain": "spain",
    "Brazil": "brazil",
    "Argentina": "argentina",
    "Portugal": "portugal",
    "England": "england"
}

TEAM_MAP = {
    "Arsenal": "阿森纳",
    "Man City": "曼城",
    "Manchester City": "曼城",
    "Liverpool": "利物浦",
    "Chelsea": "切尔西",
    "Real Madrid": "皇家马德里",
    "Barcelona": "巴塞罗那",
    "Atletico Madrid": "马德里竞技",
    "Bayern Munich": "拜仁慕尼黑",
    "PSG": "巴黎圣日耳曼",
    "Paris Saint-Germain": "巴黎圣日耳曼",
    "Tottenham Hotspur": "热刺",
    "Man Utd": "曼联",
    "Manchester United": "曼联",
    "Aston Villa": "阿斯顿维拉",
    "Newcastle United": "纽卡斯尔",
    "West Ham United": "西汉姆联",
    "Brighton and Hove Albion": "布莱顿",
    "Brentford": "布伦特福德",
    "Fulham": "富勒姆",
    "Crystal Palace": "水晶宫",
    "Nottingham Forest": "诺丁汉森林",
    "Wolverhampton Wanderers": "狼队",
    "Everton": "埃弗顿",
    "Luton Town": "卢顿",
    "Burnley": "伯恩利",
    "Sheffield United": "谢菲尔德联",
    "Bournemouth": "伯恩茅斯",
    "Girona": "赫罗纳",
    "Athletic Club": "毕尔巴鄂竞技",
    "Real Betis": "皇家贝蒂斯",
    "Real Sociedad": "皇家社会",
    "Sevilla": "塞维利亚",
    "Valencia": "瓦伦西亚",
    "Villarreal": "比利亚雷亚尔",
    "Bayer Leverkusen": "勒沃库森",
    "Stuttgart": "斯图加特",
    "RB Leipzig": "莱比锡红牛",
    "Borussia Dortmund": "多特蒙德",
    "Eintracht Frankfurt": "法兰克福",
    "Inter Milan": "国际米兰",
    "AC Milan": "AC米兰",
    "Juventus": "尤文图斯",
    "Napoli": "那不勒斯",
    "Roma": "罗马",
    "Lazio": "拉齐奥",
    "Atalanta": "亚特兰大",
    "Monaco": "摩纳哥",
    "Brest": "布雷斯特",
    "Lille": "里尔",
    "Nice": "尼斯",
    "Lens": "朗斯",
    "Marseille": "马赛",
    "Lyon": "里昂",
    "Rennes": "雷恩",
    "China": "中国",
    "Germany": "德国",
    "France": "法国",
    "Spain": "西班牙",
    "Brazil": "巴西",
    "Argentina": "阿根廷",
    "Portugal": "葡萄牙",
    "England": "英格兰"
}

COMP_MAP = {
    "Premier League": "英超",
    "UEFA Champions League": "欧冠",
    "FA Cup": "足总杯",
    "Carabao Cup": "联赛杯",
    "Community Shield": "社区盾",
    "Friendly Match": "友谊赛",
    "La Liga": "西甲",
    "Spanish La Liga": "西甲",
    "Bundesliga": "德甲",
    "German Bundesliga": "德甲",
    "Ligue 1": "法甲",
    "French Ligue 1": "法甲",
    "German DFB Cup": "德国杯"
}

# Reverse map for dropdown
CN_TO_EN_TEAMS = {v: k for k, v in TEAM_MAP.items() if k in TEAMS}
CN_TO_EN_TEAMS["所有球队"] = "All"
# Ensure National Teams are included and correctly mapped
for k in ["China", "Germany", "France", "Spain", "Brazil", "Argentina", "Portugal", "England"]:
    CN_TO_EN_TEAMS[TEAM_MAP[k]] = k

# --- Logic ---

def fetch_html(team_slug, date_str=None):
    url = f"https://www.skysports.com/{team_slug}-scores-fixtures"
    if date_str:
        url += f"/{date_str}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error: {e}")
    return None

def parse_fixtures(html, team_name):
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    fixtures = []
    elements = soup.find_all(attrs={"data-state": True})
    
    for el in elements:
        try:
            data = json.loads(el['data-state'])
            if isinstance(data, dict) and 'start' in data and 'teams' in data:
                start = data.get('start', {})
                date_str = start.get('date')
                time_str = start.get('time')
                if not date_str or not time_str: continue
                
                parts = date_str.split(' ')
                if len(parts) < 3: continue
                day = re.sub(r'(st|nd|rd|th)', '', parts[1])
                month_str = parts[2]
                
                now = datetime.now()
                dt_str = f"{now.year} {day} {month_str} {time_str}"
                try:
                    dt = datetime.strptime(dt_str, "%Y %d %B %H:%M")
                except: continue
                
                if (now - dt).days > 180: dt = dt.replace(year=now.year + 1)
                elif (dt - now).days > 180: dt = dt.replace(year=now.year - 1)
                
                uk_tz = pytz.timezone('Europe/London')
                dt_utc = uk_tz.localize(dt).astimezone(pytz.UTC)
                
                home_team = data['teams']['home']['name']['full']
                away_team = data['teams']['away']['name']['full']
                slug = TEAMS.get(team_name, "").replace("-", " ")
                
                is_home = True
                opponent = away_team
                
                if (team_name.lower() in away_team.lower().replace("-", " ")) or \
                   (slug and slug in away_team.lower().replace("-", " ")):
                    is_home = False
                    opponent = home_team
                
                fixtures.append({
                    'datetime_utc': dt_utc,
                    'opponent': opponent,
                    'competition': data.get('competition', {}).get('name', {}).get('full', 'Unknown'),
                    'team': team_name,
                    'is_home': is_home
                })
        except: continue
    return fixtures

def get_data(team_name):
    fixtures = []
    slug = TEAMS.get(team_name)
    if not slug: return []
    
    # Current month
    fixtures.extend(parse_fixtures(fetch_html(slug), team_name))
    
    # Next month
    now = datetime.now()
    next_month = now.replace(year=now.year+1, month=1, day=1) if now.month == 12 else now.replace(month=now.month+1, day=1)
    fixtures.extend(parse_fixtures(fetch_html(slug, next_month.strftime("%Y-%m-%d")), team_name))
    
    return fixtures

def get_upcoming_fixtures(team_name_cn):
    team_en = CN_TO_EN_TEAMS.get(team_name_cn, "All")
    all_fixtures = []
    
    if team_en == "All":
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(get_data, name): name for name in TEAMS.keys()}
            for f in concurrent.futures.as_completed(futures):
                all_fixtures.extend(f.result())
    else:
        all_fixtures = get_data(team_en)
        
    # Filter & Sort
    now = datetime.now(pytz.UTC)
    end_date = now + timedelta(days=7)
    upcoming = [f for f in all_fixtures if now <= f['datetime_utc'] <= end_date]
    
    # Deduplicate
    seen = set()
    unique = []
    for f in upcoming:
        key = (f['datetime_utc'], tuple(sorted([f['team'], f['opponent']])))
        if key not in seen:
            seen.add(key)
            unique.append(f)
    
    unique.sort(key=lambda x: x['datetime_utc'])
    
    # Format
    results = []
    bj_tz = pytz.timezone('Asia/Shanghai')
    for f in unique:
        dt_bj = f['datetime_utc'].astimezone(bj_tz)
        results.append({
            "time": dt_bj.strftime("%m-%d %H:%M"),
            "weekday": dt_bj.strftime("%A"),
            "team": TEAM_MAP.get(f['team'], f['team']),
            "opponent": TEAM_MAP.get(f['opponent'], f['opponent']),
            "competition": COMP_MAP.get(f['competition'], f['competition']),
            "home_away": "主" if f['is_home'] else "客"
        })
    return results

# --- UI ---

def main(page: ft.Page):
    page.title = "Football Fixtures"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#001D5C" # UCL Navy
    
    # Responsive handling
    page.window_width = 400
    page.window_height = 800

    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Text("足球赛事查询", size=24, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Football Fixtures Mobile", size=12, color="#00B2A9")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor="#0E2A6B",
        width=float("inf")
    )

    # Results List
    results_list = ft.ListView(expand=True, spacing=10, padding=20)

    def display_fixtures(fixtures):
        results_list.controls.clear()
        if not fixtures:
            results_list.controls.append(
                ft.Container(
                    content=ft.Text("未来7天无比赛", color="white70", size=16),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        else:
            weekday_map = {
                "Monday": "周一", "Tuesday": "周二", "Wednesday": "周三",
                "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日"
            }
            
            for f in fixtures:
                # Card for each match
                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{f['time']} {weekday_map.get(f['weekday'], '')}", size=12, color="#00B2A9"),
                            ft.Text(f['competition'], size=12, color="white70")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Divider(height=10, color="transparent"),
                        
                        ft.Row([
                            ft.Text(f['team'], size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Container(
                                content=ft.Text("VS", size=12, color="#00B2A9", weight=ft.FontWeight.BOLD),
                                padding=5,
                                border=ft.border.all(1, "#00B2A9"),
                                border_radius=5
                            ),
                            ft.Text(f['opponent'], size=18, weight=ft.FontWeight.BOLD, color="white")
                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        
                        ft.Divider(height=5, color="transparent"),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Text(f['home_away'], size=10, color="white"),
                                bgcolor="#0E2A6B", padding=5, border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ]),
                    padding=15,
                    bgcolor="#1A3B7C", # Slightly lighter than bg
                    border_radius=10,
                    border=ft.border.all(1, "#0E2A6B")
                )
                results_list.controls.append(card)
        page.update()

    # Dropdown
    options = [ft.dropdown.Option(k) for k in CN_TO_EN_TEAMS.keys()]
    # Sort options: Put "所有球队" first, then others
    options.sort(key=lambda x: 0 if x.key == "所有球队" else 1)
    
    team_dropdown = ft.Dropdown(
        options=options,
        value="所有球队",
        width=200,
        color="white",
        bgcolor="#0E2A6B",
        border_color="#00B2A9",
        text_size=14,
    )

    def on_refresh(e):
        loading.visible = True
        refresh_btn.disabled = True
        page.update()
        
        try:
            data = get_upcoming_fixtures(team_dropdown.value)
            display_fixtures(data)
        except Exception as ex:
            results_list.controls.clear()
            results_list.controls.append(ft.Text(f"Error: {ex}", color="red"))
        
        loading.visible = False
        refresh_btn.disabled = False
        page.update()

    refresh_btn = ft.ElevatedButton(
        "刷新赛程", 
        icon=ft.Icons.REFRESH,
        on_click=on_refresh,
        bgcolor="#00B2A9",
        color="white"
    )
    
    loading = ft.ProgressBar(width=200, color="#00B2A9", bgcolor="#0E2A6B", visible=False)

    # Layout
    page.add(
        header,
        ft.Container(
            content=ft.Column([
                ft.Row([team_dropdown, refresh_btn], alignment=ft.MainAxisAlignment.CENTER),
                loading,
                results_list
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True
        )
    )
    
    # Initial Load
    on_refresh(None)

if __name__ == "__main__":
    ft.app(target=main)
