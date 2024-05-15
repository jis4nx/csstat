import bs4
from bs4 import BeautifulSoup
from typing import Tuple
from models import Dict, Player, Ranks, Stats, Weapon, Map


async def parse_player_data(soup: BeautifulSoup) -> Player:
    rank_data = _parse_ranks(soup)
    stats = _parse_stats(soup)
    maps = _parse_maps(soup)
    weapons = _parse_weapons(soup)

    return Player(player_rank=rank_data, player_stats=stats, player_map=maps, player_weapon=weapons)


def _parse_ranks(soup: BeautifulSoup) -> Ranks:
    premier_best = soup.select_one("div.best div.cs2rating span").text.strip()
    premiere_current = soup.select_one(
        "div.rank div.cs2rating span").text.strip()
    csgo_best = soup.select(".ranks .over .best img")[-1].get("src")
    csgo_last = soup.select(".ranks .over .rank img")[-1].get("src")

    return Ranks(premier_best=premier_best, premier_current=premiere_current, csgo_best=csgo_best, csgo_last=csgo_last)


def _parse_stats(soup: BeautifulSoup) -> Stats:
    stat_div = soup.find_all("div", attrs={
                             "style": "float:left; width:60%; font-size:34px; color:#fff; line-height:0.75em; text-align:center;"})
    player_stats = [stat.text.strip() for stat in stat_div]

    win, hs, adr = player_stats
    kd_text = soup.select_one("div#kpd").text.strip()

    return Stats(win_rate=win, hs_rate=hs, adr=adr, kd=kd_text)


def _parse_maps(soup: BeautifulSoup) -> Map:
    played_map_div = soup.find_all(
        "div", attrs={"style": "background:rgba(0,0,0, 0.125); padding:0 16px;"})

    most_played_map = _parse_map_data(played_map_div[0])
    least_played_map = _parse_map_data(played_map_div[-1])

    return Map(highest_win={most_played_map[0]: most_played_map[1]}, least_win={least_played_map[0]: least_played_map[1]})


def _parse_map_data(map_div: bs4.element.Tag) -> Tuple[str, str]:
    map_text = map_div.select("span")[0].text.strip().title()
    map_image = map_div.select("img")[0].get(
        "src") or map_div.select("img")[0].get("data-cfsrc")
    return map_text, map_image


def _parse_weapons(soup: BeautifulSoup) -> Weapon:
    played_weapon_div = soup.find_all("div", class_="stat-panel")[-2]
    most, least = _parse_weapon_data(played_weapon_div)
    return Weapon(most_weapon=most, least_weapon=least)


def _parse_weapon_data(weapon_div: bs4.element.Tag) -> Tuple[Dict[str, str], Dict[str, str]]:
    most_weapon_img = weapon_div.select("img")[0].get(
        "src") or weapon_div.select("img")[0].get("data-cfsrc")
    least_weapon_img = weapon_div.select("img")[0].get(
        "src") or weapon_div.select("img")[0].get("data-cfsrc")

    most_weapon_count = weapon_div.select("span")[0].text.strip()
    least_weapon_count = weapon_div.select("span")[-1].text.strip()

    return ({most_weapon_img: most_weapon_count}, {least_weapon_img: least_weapon_count})
