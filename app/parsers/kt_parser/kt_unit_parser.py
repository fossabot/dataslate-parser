from bs4 import BeautifulSoup
from app.models.kt_unit import KtUnit


def parse_units(contents):
    soup = BeautifulSoup(contents, "lxml")
    unit_list = soup.findAll("selection", {"type": "model"})
    parsed_unit_list = []
    create_list_of_units(parsed_unit_list, unit_list)
    return parsed_unit_list


def create_list_of_units(parsed_unit_list, unit_list):
    for item in unit_list:
        parsed_unit_name = item.attrs.get("name")
        unit_profile = fetch_list_of_profiles(item)
        list_of_attributes = dict_of_attributes(unit_profile)
        list_of_keywords = get_keywords(item)
        dict_of_wargear = get_dict_of_wargear(item)
        dict_of_abilities = get_abilities(item)

        parsed_unit = KtUnit(
            name=parsed_unit_name,
            movement=list_of_attributes.get("M"),
            weapon_skill=list_of_attributes.get("WS"),
            ballistic_skill=list_of_attributes.get("BS"),
            strength=list_of_attributes.get("S"),
            toughness=list_of_attributes.get("T"),
            wounds=list_of_attributes.get("W"),
            attacks=list_of_attributes.get("A"),
            leadership=list_of_attributes.get("Ld"),
            save=list_of_attributes.get("Sv"),
            max=list_of_attributes.get("Max"),
            keywords=list_of_keywords,
            wargear=dict_of_wargear,
            abilities=dict_of_abilities
        )

        parsed_unit_list.append(parsed_unit)


def get_abilities(item):
    dict_of_abilities = {}
    list_of_unit_abilities = item.findAll("profile", {"profiletypename": "Ability"})

    for ability in list_of_unit_abilities:
        ability_name = ability.attrs.get('name')
        ability_description = ability.findAll("characteristic", {"name": "Description"})[0].attrs.get('value')
        dict_of_abilities.update({ability_name: ability_description})
    return dict_of_abilities


def get_dict_of_wargear(item):
    list_of_wargear = get_wargear(item)
    dict_of_wargear = {}
    for wargear in list_of_wargear:
        dict_of_wargear.update({wargear.get("Name"): wargear})
    return dict_of_wargear


def get_wargear(item):
    list_of_parsed_wargear = []

    list_of_possible_wargear_elements = [item for item in item.contents if item.name == "selections"][0].contents
    list_of_wargear_dicts = [selection for selection in list_of_possible_wargear_elements if selection.name]
    list_of_wargear_elements = [cleaned_weapons.contents for cleaned_weapons in list_of_wargear_dicts]

    for wargear in list_of_wargear_elements:
        wargear_profile = [wargear for wargear in wargear if wargear.name if wargear.name == "profiles"][0]
        wargear_profile_cleaned = [wargear_profile for wargear_profile in wargear_profile if wargear_profile.name]

        for wargear_profile in wargear_profile_cleaned:
            wargear_name = wargear_profile.attrs.get("name")

            wargear_profile_list = [
                wargear_profile
                for wargear_profile in wargear_profile
                if wargear_profile.name == "characteristics"][0]

            wargear_profile_list_cleaned = [
                weapon_profile_cleaned
                for weapon_profile_cleaned in wargear_profile_list
                if weapon_profile_cleaned.name == "characteristic"
            ]

            parsed_wargear = dict_of_attributes(wargear_profile_list_cleaned)
            parsed_wargear.update({"Name": wargear_name})

            list_of_parsed_wargear.append(parsed_wargear)
    return list_of_parsed_wargear


def get_keywords(item):
    keyword_list = []
    keywords = [item for item in item.contents if item.name == "categories"][0].contents
    cleaned_keywords = [keyword for keyword in keywords if keyword.name]
    for keyword in cleaned_keywords:
        keyword_list.append(keyword.attrs.get("name"))
    return keyword_list


def fetch_list_of_profiles(item):
    unit_profile = item.findAll("profile", {"profiletypename": "Model"})[0].contents

    list_of_characteristics = [
        selected_unit
        for selected_unit in unit_profile
        if selected_unit.name == "characteristics"][0].contents

    cleaned_list_of_characteristics = [
        selected_unit
        for selected_unit in list_of_characteristics
        if selected_unit.name == "characteristic"]

    return cleaned_list_of_characteristics


def dict_of_attributes(item):
    dict_of_attrs = {}
    for attribute in item:
        attr_name = attribute.get("name")
        attr_value = attribute.get("value")
        dict_of_attrs.update({attr_name: attr_value})
    return dict_of_attrs