import codecs, re
import unicodecsv as csv

# Save the file with UTF-8 BOM encoding

# These columns may vary depending on what pops you have added to the game
# Change as necessary
id_column = 0
name_column = 14
culture_column = 1
religion_column = 2
tradegoods_column = 3
civilization_column = 12
barbarian_column = 13
province_rank_column = 13
area_column = 16
# Pop values
citizen_column = 4
freemen_column = 4
slaves_column = 9
tribesmen_column = 10
# Pops for the 1815 mod
lower_strata_column = 6
middle_strata_column = 7
upper_strata_column = 11
proletariat_column = 8
# Extra minority pops, beginning with pop type column
extra_pop1 = 20
extra_pop2 = 24
extra_pop3 = 28
extra_pops = [extra_pop1, extra_pop2, extra_pop3]
# Add these values to above minority pop columns to get corresponding data
culture = 1
religion = 2
size = 3

terrain_file = open("province_terrain/00_province_terrain.txt",encoding="utf=8")

def create_terrain_dict(terrain_file):
    terrain_txt = terrain_file.read()
    terrain_dict = {}
    for line in terrain_txt.splitlines(True):
        if line:
            key, value = map(str.strip, line.split("="))
            terrain_dict[key] = value
    return terrain_dict
    # This makes a VERY BIG DICT. Do NOT try to look at it
    # or you will unleash a cosmic terror

terrain_dict = create_terrain_dict(terrain_file)

def find_terrain(province_id):
    pass

setup_csv = open("province_setup.csv", "rb")
reader = csv.reader(setup_csv, delimiter=";")

generated_setup = codecs.open("GENERATED_SETUP.txt", "w", "utf-8-sig")

non_habitable_provinces = open("../map_data/default.map")
non_habitable_provinces_data = non_habitable_provinces.read()
pattern = "RANGE {(.*)}"
non_habitable_ranges = re.findall(pattern, non_habitable_provinces_data)
non_habitable_ranges = [i.split(" ") for i in non_habitable_ranges]
new_non_habitable_ranges = []
for x in non_habitable_ranges:
    x = [i for i in x if i]
    new_non_habitable_ranges.append(x)
non_habitable_ranges = new_non_habitable_ranges

def check_if_habitable(province_id):
    # Check if the province ID is any of the ranges specified
    try:
        province_id = int(province_id)
    except:
        return False
    for province_range in non_habitable_ranges:
        if province_id >= int(province_range[0]) and province_id <= int(province_range[1]):
            return True
    if " " + str(province_id) not in non_habitable_provinces:
        return True
    else:
        return False
    
    

with generated_setup as f:
    for row in reader:
        # Ignore seazones, wastelands, impassables, lakes, rivers etc.
        if check_if_habitable(row[id_column]):
            if row[id_column] in terrain_dict:
                terrain = terrain_dict[row[id_column]]
            else:
                terrain = ""
            province_rank = row[province_rank_column]
            if province_rank == "0":
                province_rank = "settlement"
            elif province_rank == "1":
                province_rank = "city"
            
            f.write(
        row[id_column] + '={ #' + row[name_column] + '\n' +
        '   terrain="' + terrain + '"\n' +
        '   culture="' + row[culture_column] + '"\n' +
        '   religion="' + row[religion_column] + '"\n' +
        '   trade_goods="' + row[tradegoods_column] + '"\n' +
        '   civilization_value=' + row[civilization_column] + '\n' +
        '   barbarian_power=' + row[barbarian_column] + '\n' +
        '   province_rank="' + province_rank + '"\n'
            )
            if row[citizen_column] != "0":
                f.write(
        '   citizen={\n' +
        '      amount=' + row[citizen_column] + '\n'
        '   }\n'
                )
            if row[freemen_column] != "0":
                f.write(
        '   freemen={\n' +
        '      amount=' + row[freemen_column] + '\n'
        '   }\n' 
                )
            if row[slaves_column] != "0":
                f.write(
        '   slaves={\n' +
        '      amount=' + row[slaves_column] + '\n'
        '   }\n' 
                )
            if row[tribesmen_column] != "0":
                f.write(
        '   tribesmen={\n' +
        '      amount=' + row[tribesmen_column] + '\n'
        '   }\n' 
                )
        # Below special for 1815 mod
            if row[lower_strata_column] != "0":
                f.write(
        '   lower_strata={\n' +
        '      amount=' + row[lower_strata_column] + '\n'
        '   }\n' 
                )
            if row[middle_strata_column] != "0":
                f.write(
        '   middle_strata={\n' +
        '      amount=' + row[middle_strata_column] + '\n'
        '   }\n' 
                )
            if row[upper_strata_column] != "0":
                f.write(
        '      upper_strata={\n' +
        '         amount=' + row[upper_strata_column] + '\n'
        '   }\n' 
                )
            if row[proletariat_column] != "0":
                f.write(
        '   proletariat={\n' +
        '      amount=' + row[proletariat_column] + '\n'
        '   }\n' 
                )
        # Only look at extra pops if there is data there
            for extra_pop in extra_pops:
                if row[extra_pop] != "" and len(row[extra_pop]) < 13:
                    f.write(
            '   ' + row[extra_pop].replace(" ","_") + '={\n' +
            '       amount=' + row[extra_pop+size] + '\n' +
            '       culture="' + row[extra_pop+culture] + '"\n' +
            '       religion="' + row[extra_pop+religion] + '"\n' +
            '   }\n'
                )
        # Remove above if not using this for the 1815 mod
            f.write(
        '}\n\n'
            )
