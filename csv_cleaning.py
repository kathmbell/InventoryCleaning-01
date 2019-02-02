import pandas as pd
import re


df = pd.read_csv('Cannabis Product Pricing Data 010419.csv')
df=df.dropna(subset=['Product_Name'])
df=df.dropna(subset=['Product_Type'])
df=df.dropna(subset=['Price'])
df=df[~df['Product_Type'].str.contains("Accessory")]
df=df[~df['Product_Type'].str.contains("Cartridge")]
df=df[~df['Product_Type'].str.contains("Clone")]
df=df[~df['Product_Type'].str.contains("Other")]
df=df[~df['Product_Type'].str.contains("PreRoll")]
df=df[~df['Product_Type'].str.contains("Seeds")]
df=df[~df['Product_Type'].str.contains("Topical")]

df = df[~df['Product_Name'].str.contains('sample')]
df = df[~df['Product_Name'].str.contains('Sample')]
df = df[~df['Product_Name'].str.contains('SAMPLE')]
to_drop = ['Sample', 'sample']

df_cities = pd.read_csv('uscitiesv1.4.csv')

def eachedible(row):
    address = str(row['Company_Address'])
    state = re.findall('[A-Z]{2}', address)
    if state==[]:
        state.append('')
        addcity = ['']
        addlat = ['']
        addlang = ['']
    else:
        filtered_cities = df_cities[df_cities.state_id == state[-1]]
        all_cities = list(filtered_cities.city)
        all_lats = list(filtered_cities.lat)
        all_langs = list(filtered_cities.lng)
        addcity = ['']
        addlat = ['']
        addlang = ['']
        for i in range(len(all_cities)):
            city = all_cities[i]
            if city in address:
                addcity.append(city)
                addlat.append(all_lats[i])
                addlang.append(all_langs[i])
    product = str(row['Product_Type'])
    default1 = row['Quantity']
    default2 = row['Quantity_Type']
    if product=='Edible':
        return pd.Series(['Each', 'Each', 'US-'+state[-1], addcity[-1], (addlat[-1], addlang[-1])]) #state should be US-CA
    else:
        return pd.Series([default1, default2, 'US-'+state[-1], addcity[-1], (addlat[-1], addlang[-1])])
df[['Quantity', 'Quantity_Type', 'State', 'City', 'Lat,Long']] = df.apply(eachedible, axis=1)

df=df.dropna(subset=['Product_Type'])
df=df.drop(['Input_URL'], axis=1)
df.to_csv('test_2.csv')
print(df.head())
#print(list(dataFrame))
