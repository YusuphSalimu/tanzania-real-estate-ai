#!/usr/bin/env python3
"""
Generate comprehensive sample data for Tanzania Real Estate AI
Includes properties for all regions, rental rooms, and contact information
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Tanzania regions with real locations
regions_data = {
    'Dar es Salaam': {
        'locations': ['Moroco', 'Ilala', 'Temeke', 'Buza', 'Mbweni', 'Majohe', 'Kigogo', 'Kiwalani', 'Gongo la Mboto', 'Kariakoo', 'Kisutu', 'Mchikichini', 'Segerea', 'Tabata', 'Ukonga', 'Vingunguti', 'Bunju', 'Goba', 'Hananasif', 'Kawe', 'Kimara', 'Kunduchi', 'Magomeni', 'Majengo', 'Makumbusho', 'Manzese', 'Masaki', 'Mikocheni', 'Mlimani', 'Msasani', 'Mwenge', 'Oysterbay', 'Regent', 'Salasala', 'Sinza', 'Tandale', 'Tegeta', 'Wazo', 'Mabwepande', 'Makongo', 'Mbezi', 'Kibaha', 'Kisewe', 'Mazizini', 'Mikwambe', 'Mpiji', 'Msongola', 'Mwongo', 'Mzinga', 'Pongwe', 'Urambo', 'Vikongoto'],
        'price_multiplier': 1.5
    },
    'Arusha': {
        'locations': ['Elerai', 'Engaresero', 'Esso', 'Kijenge', 'Kilimani', 'Kimandolu', 'Kisongo', 'Majengo', 'Moshi', 'Naura', 'Ngarenaro', 'Olmotonyi', 'Sekei', 'Sokon I', 'Sokon II', 'Themi', 'Unga Limited', 'Uswahilini', 'Njiro', 'Arusha Meru', 'Tengeru', 'Old Moshi', 'Levolosi'],
        'price_multiplier': 1.2
    },
    'Dodoma': {
        'locations': ['Maili Mbili', 'Mipango', 'Chinangali I', 'Chinangali II', 'Huduma', 'Izenga', 'Kikuyu', 'Madukani', 'Makole', 'Mji Mwema', 'Mlimwa', 'Nala', 'Nzuguni', 'Swaswa', 'Vikongoto', 'Zuzu', 'Bahi', 'Bihawana', 'Chamwino', 'Hombolo', 'Ihanda', 'Ihumwa', 'Kikombo', 'Lukali', 'Msalato', 'Mzeru', 'Ntomoko', 'Rudi', 'Zanka'],
        'price_multiplier': 0.8
    },
    'Mwanza': {
        'locations': ['Ilemela', 'Kirumba', 'Mabatini', 'Machinjoni', 'Makongoro', 'Mchanganyiko', 'Mkolani', 'Nyakato', 'Pasiansi', 'Pamba', 'Shinyanga', 'Tunduma', 'Ukerewe', 'Bugogwa', 'Bulombora', 'Buswelu', 'Isamilo', 'Kabangaja', 'Kagondo', 'Kahama', 'Kasulu', 'Kisesa', 'Kitete', 'Kwigulango', 'Mabale', 'Mabuki', 'Makoko', 'Malya', 'Mchukwi', 'Nyakasanga'],
        'price_multiplier': 1.1
    },
    'Mbeya': {
        'locations': ['Iyunga', 'Isyangati', 'Shinyanga', 'Uyole', 'Mabonde', 'Mbalizi', 'Mwambani', 'Nsalaga', 'Soweto', 'Uwanza', 'Zimamoto', 'Igumbilo', 'Rungwe', 'Kyela', 'Lufilo', 'Matema', 'Mwakaleli', 'Ngana', 'Nsongwe', 'Itope', 'Ileje', 'Isongole', 'Kamsamba', 'Kapeni', 'Kasanga', 'Kasumulu', 'Kawelonde', 'Kikwe', 'Kipeta', 'Lubanda', 'Lugala', 'Lukulu', 'Lupingu', 'Mwaya', 'Nkansi', 'Nkanga', 'Nkombwe', 'Nkonji', 'Nsunga', 'Nyambala'],
        'price_multiplier': 0.9
    },
    'Tanga': {
        'locations': ['Chumbageni', 'Kirongo', 'Mabawa', 'Mafuriko', 'Maji Maji', 'Makorora', 'Maringeni', 'Mkuzi', 'Ngamiani Kati', 'Ngamiani Kusini', 'Nguvu Kuu', 'Pongwe', 'Tongoni', 'Usagara', 'Ziwani', 'Mkinga', 'Kwangwazi', 'Mabogini', 'Magogoni', 'Makanya', 'Mnyuzi', 'Mpirani', 'Amani', 'Bwembwera', 'Kigombe', 'Magila', 'Bombo', 'Kikokwe', 'Makuyuni', 'Mwera', 'Ushongwe', 'Handeni', 'Kwagunda', 'Mabanda', 'Mgambo'],
        'price_multiplier': 0.85
    },
    'Morogoro': {
        'locations': ['Bigwa', 'Boma', 'Kihonda', 'Kichangani', 'Mikese', 'Mzinga', 'Saba Saba', 'Tungi', 'Uchanganyiko', 'Bungu', 'Dutu', 'Kilakala', 'Kiroka', 'Kisaki', 'Lukobe', 'Mgeta', 'Mlali', 'Mvomero', 'Ngerengere', 'Ruvuma', 'Turu', 'Mvomero', 'Dutu', 'Kilakala', 'Kiroka', 'Kisaki', 'Lukobe', 'Mgeta', 'Mikese', 'Mlali', 'Ngerengere', 'Kilosa', 'Kidodi', 'Kilangali', 'Magubike', 'Mikumi', 'Kilombero', 'Ifakara', 'Kidatu', 'Ulanga'],
        'price_multiplier': 0.9
    },
    'Mtwara': {
        'locations': ['Chongoleani', 'Jangwani', 'Kichakani', 'Kihanga', 'Kijiji cha Kati', 'Kisanga', 'Magomeni', 'Mapogoro', 'Mikindani', 'Naliendele', 'Shangani', 'Ujembe', 'Utenge', 'Chilulu', 'Chimboto', 'Masasi', 'Nanyumbu', 'Tandahimba', 'Newala', 'Naliendele', 'Mikindani', 'Magomeni', 'Kisanga', 'Chongoleani', 'Jangwani'],
        'price_multiplier': 0.8
    },
    'Ruvuma': {
        'locations': ['Songea Mjini', 'Songea Mjini Kati', 'Songea Mjini Kusini', 'Songea Mjini Mashariki', 'Songea Mjini Magharibi', 'Matengo', 'Ruangwa', 'Mchuku', 'Madaba', 'Namtumbo', 'Mbinga', 'Nyasa', 'Matengo Street', 'Ruangwa', 'Mchuku', 'Mjini Kati', 'Songea'],
        'price_multiplier': 0.7
    },
    'Kigoma': {
        'locations': ['Kigoma', 'Kigoma Ujiji', 'Buhingu', 'Bubango', 'Gungu', 'Kagongo', 'Mabanda', 'Mwanga', 'Rusumo', 'Ujiji', 'Kasulu', 'Kibondo', 'Buhigwe', 'Uvinza', 'Ujiji', 'Kigoma', 'Buhingu', 'Kagongo', 'Mwanga', 'Rusumo'],
        'price_multiplier': 0.75
    },
    'Tabora': {
        'locations': ['Kigoma', 'Kikuyu', 'Mita', 'Mwanza', 'Ngalula', 'Nkundi', 'Shinyanga', 'Urambo', 'Zambia', 'Uyui', 'Nzega', 'Igunga', 'Sikonge', 'Mwanza Street', 'Kigoma', 'Kikuyu', 'Mita', 'Ngalula', 'Urambo'],
        'price_multiplier': 0.7
    },
    'Singida': {
        'locations': ['Mji Mwema', 'Mjini', 'Mungumaji', 'Nkungi', 'Singida', 'Singida Mjini', 'Ikungi', 'Manyoni', 'Iramba', 'Mkalama', 'Mji Mwema', 'Mjini', 'Mungumaji', 'Nkungi', 'Singida'],
        'price_multiplier': 0.65
    },
    'Pwani': {
        'locations': ['Bagamoyo', 'Chalinze', 'Kibaha', 'Kisarawe', 'Mkuranga', 'Rufiji', 'Kibaha', 'Bagamoyo', 'Chalinze', 'Kisarawe', 'Kibaha', 'Bagamoyo', 'Mkuranga', 'Kisarawe', 'Rufiji'],
        'price_multiplier': 0.8
    },
    'Unguja': {
        'locations': ['Stone Town', 'Forodhani', 'Shangani', 'Mkunazini', 'Mwembesongo', 'Mwanakwerekwe', 'Mwera', 'Mwera Kuu', 'Mwera Ndogo', 'Mwera Mchanga', 'Bumbwini', 'Chwaka', 'Donge', 'Fujoni', 'Jongowe', 'Kiwengwa', 'Kiwengwa Pwani', 'Kiwengwa Mchanga', 'Kiwengwa Kuu', 'Kiwengwa Ndogo', 'Kijini', 'Matemwe', 'Nungwi', 'Paje', 'Uroa', 'Bwejuu', 'Jambiani', 'Kizimkazi', 'Mchangani', 'Michamvi'],
        'price_multiplier': 1.3
    },
    'Pemba': {
        'locations': ['Chake Chake', 'Wete', 'Micheweni', 'Mkoani', 'Chake Chake', 'Wete', 'Micheweni', 'Mkoani'],
        'price_multiplier': 1.1
    },
    'Iringa': {
        'locations': ['Iringa Mjini', 'Mkwawa', 'Mkwakwani', 'Nyangoro', 'Ilula', 'Mkulanga', 'Igeleke', 'Kihesa', 'Ruaha', 'Iringa'],
        'price_multiplier': 0.85
    },
    'Kilimanjaro': {
        'locations': ['Moshi', 'Hai', 'Rombo', 'Mwanga', 'Same', 'Siha', 'Marangu', 'Kibosho', 'Uru', 'Old Moshi', 'Kibonoto', 'Machame', 'Ngorongoro', 'Karatu', 'Mto wa Mbu'],
        'price_multiplier': 1.0
    },
    'Manyara': {
        'locations': ['Babati', 'Kiteto', 'Simanjiro', 'Mbulu', 'Hanang', 'Babati', 'Mbugwe', 'Mbuyu', 'Mwada', 'Magugu', 'Katesh', 'Basotu', 'Dareda', 'Endanach', 'Gidamilanda', 'Haydom', 'Kwaraa', 'Mangola', 'Mwada'],
        'price_multiplier': 0.75
    },
    'Rukwa': {
        'locations': ['Sumbawanga', 'Nkasi', 'Mpanda', 'Laela', 'Kalambo', 'Sumbawanga', 'Karema', 'Matai', 'Mwese', 'Kasanga', 'Kagunga', 'Kipamba', 'Mwambezi', 'Nkamba', 'Rungwa', 'Usevya'],
        'price_multiplier': 0.6
    },
    'Katavi': {
        'locations': ['Mpanda', 'Mlele', 'Nsimbo', 'Mpanda', 'Kasanga', 'Kagunga', 'Kipampa', 'Karema', 'Mishamo', 'Ibindi', 'Uvinza', 'Mwese', 'Usevya'],
        'price_multiplier': 0.65
    },
    'Njombe': {
        'locations': ['Njombe', 'Wanging\'ombe', 'Makete', 'Ludewa', 'Njombe', 'Igosi', 'Ilembula', 'Lupanga', 'Madunda', 'Manda', 'Matengo', 'Mlandizi', 'Mwanga', 'Njoka', 'Uwemba'],
        'price_multiplier': 0.7
    },
    'Lindi': {
        'locations': ['Lindi', 'Nachingwea', 'Ruangwa', 'Kilwa', 'Nachingwea', 'Liwale', 'Lindi', 'Nachingwea', 'Ruangwa', 'Kilwa', 'Kilwa Kivinje', 'Kilwa Masoko', 'Somanga', 'Nanhyanga', 'Mitole'],
        'price_multiplier': 0.65
    },
    'Mara': {
        'locations': ['Musoma', 'Serengeti', 'Tarime', 'Butiama', ' Rorya', 'Musoma', 'Bukiri', 'Mugumu', 'Kijiji cha Wazee', 'Mwalimu', 'Nungwi', 'Kiroka', 'Muganza', 'Sukuma', 'Itena', 'Maburi', 'Nyamongo'],
        'price_multiplier': 0.8
    },
    'Shinyanga': {
        'locations': ['Shinyanga', 'Kahama', 'Kishapu', 'Bukombe', 'Shinyanga', 'Mwanhala', 'Ilemela', 'Ndala', 'Mwadui', 'Kahama', 'Kishapu', 'Bukombe', 'Uyui', 'Mabama', 'Malampaka', 'Mwasele'],
        'price_multiplier': 0.75
    },
    'Simiyu': {
        'locations': ['Bariadi', 'Maswa', 'Meatu', 'Bariadi', 'Mwanhuzi', 'Malampaka', 'Mwabayuhi', 'Nyalikungu', 'Sogea', 'Mwandugu', 'Mwanhuzi', 'Bariadi', 'Maswa', 'Meatu'],
        'price_multiplier': 0.7
    },
    'Geita': {
        'locations': ['Geita', 'Bukombe', 'Chato', 'Mbogwe', 'Nyang\'hwale', 'Geita', 'Bukombe', 'Chato', 'Mbogwe', 'Nyang\'hwale', 'Katoro', 'Kahama', 'Mwandiga', 'Nzera', 'Sikonge'],
        'price_multiplier': 0.7
    },
    'Songwe': {
        'locations': ['Vwawa', 'Mbozi', 'Ileje', 'Mbarali', 'Chunya', 'Vwawa', 'Mlowo', 'Igurusi', 'Isaka', 'Kamsamba', 'Mlowo', 'Vwawa', 'Mbozi', 'Ileje', 'Mbarali', 'Chunya'],
        'price_multiplier': 0.65
    }
}

# Property types with their characteristics
property_types = {
    # For Sale
    'House': {'min_price': 80000000, 'max_price': 500000000, 'min_size': 80, 'max_size': 400, 'min_bed': 2, 'max_bed': 6, 'min_bath': 1, 'max_bath': 4},
    'Apartment': {'min_price': 60000000, 'max_price': 300000000, 'min_size': 60, 'max_size': 250, 'min_bed': 1, 'max_bed': 4, 'min_bath': 1, 'max_bath': 3},
    'Villa': {'min_price': 200000000, 'max_price': 1000000000, 'min_size': 200, 'max_size': 600, 'min_bed': 3, 'max_bed': 8, 'min_bath': 2, 'max_bath': 6},
    'Townhouse': {'min_price': 100000000, 'max_price': 400000000, 'min_size': 120, 'max_size': 300, 'min_bed': 2, 'max_bed': 5, 'min_bath': 1, 'max_bath': 3},
    'Bungalow': {'min_price': 70000000, 'max_price': 350000000, 'min_size': 100, 'max_size': 350, 'min_bed': 2, 'max_bed': 5, 'min_bath': 1, 'max_bath': 3},
    
    # For Rent (Monthly)
    'Master_Room': {'min_price': 80000, 'max_price': 500000, 'min_size': 15, 'max_size': 30, 'min_bed': 1, 'max_bed': 1, 'min_bath': 1, 'max_bath': 1},
    'Single_Room': {'min_price': 40000, 'max_price': 200000, 'min_size': 10, 'max_size': 20, 'min_bed': 1, 'max_bed': 1, 'min_bath': 0, 'max_bath': 1},
    'Bedsitter': {'min_price': 60000, 'max_price': 300000, 'min_size': 20, 'max_size': 35, 'min_bed': 1, 'max_bed': 1, 'min_bath': 1, 'max_bath': 1},
    '1_Bedroom_Apt': {'min_price': 150000, 'max_price': 800000, 'min_size': 35, 'max_size': 60, 'min_bed': 1, 'max_bed': 1, 'min_bath': 1, 'max_bath': 1},
    '2_Bedroom_Apt': {'min_price': 250000, 'max_price': 1200000, 'min_size': 50, 'max_size': 90, 'min_bed': 2, 'max_bed': 2, 'min_bath': 1, 'max_bath': 2},
    '3_Bedroom_Apt': {'min_price': 400000, 'max_price': 2000000, 'min_size': 70, 'max_size': 120, 'min_bed': 3, 'max_bed': 3, 'min_bath': 2, 'max_bath': 3},
    'Studio_Apartment': {'min_price': 100000, 'max_price': 600000, 'min_size': 25, 'max_size': 45, 'min_bed': 1, 'max_bed': 1, 'min_bath': 1, 'max_bath': 1},
    'Guest_House': {'min_price': 300000, 'max_price': 1500000, 'min_size': 80, 'max_size': 200, 'min_bed': 2, 'max_bed': 4, 'min_bath': 1, 'max_bath': 3},
    'Hotel_Room': {'min_price': 200000, 'max_price': 1000000, 'min_size': 20, 'max_size': 40, 'min_bed': 1, 'max_bed': 1, 'min_bath': 1, 'max_bath': 1}
}

# Sample owner names and contact info
owner_names = [
    'John Mwangi', 'Aisha Hassan', 'Peter Kimario', 'Grace Mbeya', 'Joseph Mlay',
    'Sarah Kileo', 'David Msangi', 'Elizabeth Mwangaza', 'Michael Nyoni', 'Fatuma Ali',
    'Robert Kalenga', 'Zawadi Msemwa', 'James Mkenda', 'Anna Massawe', 'George Mgaya',
    'Miriam Kessy', 'Thomas Mcharo', 'Susan Kiwanga', 'Frank Mwanga', 'Joyce Mlay'
]

# Generate sample data
def generate_sample_data():
    properties = []
    property_id = 1
    
    for region, region_data in regions_data.items():
        locations = region_data['locations']
        price_multiplier = region_data['price_multiplier']
        
        # Generate 5-10 properties per region
        num_properties = random.randint(5, 10)
        
        for _ in range(num_properties):
            # Random location
            location = random.choice(locations)
            
            # Random property type
            property_type = random.choice(list(property_types.keys()))
            
            # Determine listing type based on property type
            if property_type in ['Master_Room', 'Single_Room', 'Bedsitter', '1_Bedroom_Apt', '2_Bedroom_Apt', '3_Bedroom_Apt', 'Studio_Apartment', 'Guest_House', 'Hotel_Room']:
                listing_type = 'rent'
            else:
                listing_type = random.choice(['sale', 'rent'])
            
            # Get property characteristics
            props = property_types[property_type]
            
            # Generate property details
            bedrooms = random.randint(props['min_bed'], props['max_bed'])
            bathrooms = random.randint(props['min_bath'], props['max_bath'])
            size_sqm = random.randint(props['min_size'], props['max_size'])
            
            # Calculate price based on region and property type
            base_price = random.randint(props['min_price'], props['max_price'])
            price_tzs = int(base_price * price_multiplier)
            
            # Adjust price for size and bedrooms
            if listing_type == 'sale':
                price_tzs = int(price_tzs * (1 + (size_sqm / 100) * 0.1) * (1 + bedrooms * 0.05))
            else:  # rent
                price_tzs = int(price_tzs * (1 + (size_sqm / 50) * 0.05) * (1 + bedrooms * 0.03))
            
            # Random owner info
            owner_name = random.choice(owner_names)
            owner_phone = f"+255 {random.choice([7, 6])}{random.randint(10000000, 99999999)}"
            owner_email = f"{owner_name.lower().replace(' ', '.')}@example.com"
            
            # Random amenities
            all_amenities = ['Parking', 'Security', 'Water', 'Electricity', 'WiFi', 'Air Conditioning', 'Balcony', 'Garden', 'Storage', 'Elevator', 'Gym', 'Pool', 'Backup Generator', 'Solar Water Heater', 'Built-in Wardrobes', 'Kitchen Cabinets', 'Ceramic Tiles', 'Aluminum Windows', 'Gated Community', 'Playground']
            num_amenities = random.randint(3, 8)
            amenities = ', '.join(random.sample(all_amenities, num_amenities))
            
            # Random description
            descriptions = [
                f"Beautiful {property_type.replace('_', ' ').title()} located in {location}, {region}. Perfect for {'family' if bedrooms > 2 else 'individuals'} with {bedrooms} bedrooms and modern amenities.",
                f"Spacious {property_type.replace('_', ' ').title()} in the heart of {location}. Features {bedrooms} bedrooms, {bathrooms} bathrooms, and {size_sqm} sqm of living space.",
                f"Modern {property_type.replace('_', ' ').title()} in {location}, {region}. Excellent condition with recent renovations. Ideal location with easy access to amenities.",
                f"Well-maintained {property_type.replace('_', ' ').title()} offering {bedrooms} bedrooms in {location}. Close to schools, hospitals, and shopping centers.",
                f"Stunning {property_type.replace('_', ' ').title()} with {size_sqm} sqm of space. Located in the desirable {location} neighborhood of {region}."
            ]
            description = random.choice(descriptions)
            
            # Create property
            property_data = {
                'id': property_id,
                'location': location,
                'city': region,
                'ward': location,
                'district': location,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'size_sqm': size_sqm,
                'property_type': property_type,
                'listing_type': listing_type,
                'price_tzs': price_tzs,
                'description': description,
                'amenities': amenities,
                'owner_name': owner_name,
                'owner_phone': owner_phone,
                'owner_email': owner_email,
                'latitude': -6.0 + random.uniform(-5, 5),  # Approximate Tanzania coordinates
                'longitude': 35.0 + random.uniform(-5, 5),
                'created_at': datetime.now() - timedelta(days=random.randint(1, 365)),
                'status': 'available'
            }
            
            properties.append(property_data)
            property_id += 1
    
    return properties

# Generate and save data
if __name__ == "__main__":
    print("Generating comprehensive Tanzania real estate data...")
    
    properties = generate_sample_data()
    
    # Convert to DataFrame
    df = pd.DataFrame(properties)
    
    # Save to CSV
    df.to_csv('../data/sample_data_comprehensive.csv', index=False)
    
    print(f"Generated {len(properties)} properties across {len(regions_data)} regions")
    print(f"Data includes {len(df[df['listing_type'] == 'sale'])} properties for sale")
    print(f"Data includes {len(df[df['listing_type'] == 'rent'])} rental properties")
    print(f"Saved to: ../data/sample_data_comprehensive.csv")
    
    # Display sample statistics
    print("\nSample Statistics:")
    print(f"Average sale price: TZS {df[df['listing_type'] == 'sale']['price_tzs'].mean():,.0f}")
    print(f"Average rent price: TZS {df[df['listing_type'] == 'rent']['price_tzs'].mean():,.0f}/month")
    print(f"Price range: TZS {df['price_tzs'].min():,.0f} - TZS {df['price_tzs'].max():,.0f}")
    
    # Show sample properties
    print("\nSample Properties:")
    for _, prop in df.head(3).iterrows():
        listing_type = "For Sale" if prop['listing_type'] == 'sale' else f"For Rent: TZS {prop['price_tzs']:,}/month"
        print(f"• {prop['property_type']} in {prop['location']}, {prop['city']} - {listing_type}")
    
    print("\nData generation complete!")
