import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

TRANSPORT_INFO = {
    "Santo Domingo": {
        "options": ["Uber (widely available)", "Metro Line 1 & 2 (~$0.35/ride)", "Carros públicos (shared taxis)", "Motoconcho (motorcycle taxi — adventurous!)"],
        "tip": "Uber is safest and easiest for tourists. Metro is great for crossing the city cheaply."
    },
    "Punta Cana": {
        "options": ["Uber (available)", "Resort shuttles", "Moto-taxi for short distances", "Rental car recommended for exploring"],
        "tip": "Most resorts are spread out — a rental car gives you freedom to explore local beaches."
    },
    "Santiago": {
        "options": ["Uber (available)", "Carros públicos", "Motoconcho"],
        "tip": "Carros públicos run fixed routes and are very cheap (~$0.50). Ask locals for routes."
    },
    "Puerto Plata": {
        "options": ["Uber (limited)", "Motoconcho", "Rental car", "Local taxis"],
        "tip": "Rent a car or scooter to explore the coast freely. Motoconchos are cheap for short trips."
    },
    "Samaná": {
        "options": ["Rental car", "Motoconcho", "Boat taxis (for Las Galeras/Las Terrenas)"],
        "tip": "A rental car is highly recommended in Samaná. Boat taxis connect the peninsula's beach towns."
    },
    "La Romana": {
        "options": ["Resort shuttles", "Uber (limited)", "Local taxis", "Rental car"],
        "tip": "Most attractions are resort-based. Taxis are negotiated flat rates — agree before you ride."
    },
    "San Juan": {
        "options": ["Uber (widely available)", "AMA Bus (~$0.75/ride)", "Ferry to Cataño ($0.50)", "Walking in Old San Juan"],
        "tip": "Old San Juan is very walkable. Take the free trolley between city gates."
    },
    "Ponce": {
        "options": ["Uber (available)", "Local taxis", "Walking in historic center"],
        "tip": "The historic center is compact and walkable. Uber is reliable for trips to outlying areas."
    },
    "Rincón": {
        "options": ["Rental car (essential)", "Uber (very limited)", "Local taxis"],
        "tip": "A rental car is essential in Rincón — public transport is very limited here."
    },
    "Vieques": {
        "options": ["Golf carts (popular rental)", "Rental car", "Scooter rental", "Taxis"],
        "tip": "Golf carts are the classic Vieques transport. Rent one at the ferry terminal."
    },
    "Culebra": {
        "options": ["Golf cart rental", "Walking", "Water taxis to beaches"],
        "tip": "Culebra is tiny — most things are walkable from town. Golf carts handle the hilly roads."
    },
    "Cartagena": {
        "options": ["Uber (available)", "Cabify", "Tuk-tuks in the old city", "Horse-drawn carriages (touristy but fun)", "Walking in Walled City"],
        "tip": "The Walled City is best explored on foot. Tuk-tuks are great for short hops."
    },
    "Medellín": {
        "options": ["Uber (available)", "Metro (~$0.80/ride)", "Metro Cable (connects hillside neighborhoods)", "Cabify"],
        "tip": "Medellín's Metro system is clean, safe, and affordable. The cable car gives stunning city views."
    },
    "Bogotá": {
        "options": ["Uber (available)", "TransMilenio BRT (~$0.70/ride)", "Cabify", "Bike share (BiciBogotá)"],
        "tip": "TransMilenio covers most of the city. Uber/Cabify are safer for nighttime travel."
    },
    "Santa Marta": {
        "options": ["Uber (available)", "Local taxis", "Rental car for Tayrona", "Motoconcho"],
        "tip": "Taxis are plentiful and cheap. A rental car is best for reaching Tayrona National Park."
    },
    "Cali": {
        "options": ["Uber (available)", "MIO Bus (~$0.80/ride)", "Cabify", "Local taxis"],
        "tip": "MIO covers the main corridors. Uber and Cabify are recommended for evening travel."
    },
    "Mexico City": {
        "options": ["Uber (widely available)", "Metro (~$0.25/ride)", "Metrobús", "Cabify", "Walking in Roma/Condesa/Centro"],
        "tip": "Mexico City's metro is one of the cheapest in the world. Uber is reliable for late nights."
    },
    "Cancún": {
        "options": ["Uber (available)", "ADO Bus (to Tulum/Playa ~$8-15)", "R1/R2 local buses ($0.60)", "Rental car for flexibility"],
        "tip": "The hotel zone is long and walkable only in sections. Local R1/R2 buses run the full strip cheaply."
    },
    "Tulum": {
        "options": ["Rental bike or scooter (most popular)", "Uber (limited)", "Colectivos to Playa del Carmen (~$3)", "Rental car"],
        "tip": "Tulum's town and beach zone are 3km apart. Renting a bike or scooter is the most common way to get around."
    },
    "Oaxaca": {
        "options": ["Walking in historic center", "Uber (available)", "Local taxis", "Colectivos for day trips"],
        "tip": "The historic center is very walkable. Colectivos are cheap for reaching nearby villages and ruins."
    },
    "Puerto Vallarta": {
        "options": ["Uber (available)", "Local buses (~$0.60)", "Water taxi to beaches", "Walking on the Malecón"],
        "tip": "Water taxis are the best way to reach secluded beaches south of town. The Malecón is fully walkable."
    },
    "Playa del Carmen": {
        "options": ["Walking on 5th Avenue", "Uber (available)", "Colectivos to Tulum (~$3)", "ADO Bus"],
        "tip": "5th Avenue and the beach are walkable. Colectivos are cheap for day trips to Tulum or Cancún."
    },
}


def get_mock_for_city(city: str, destination: str) -> dict:
    """
    Return city-specific mock data when OpenAI is unavailable.
    Each city gets its own unique set of recommendations.
    """

    city_lower = city.lower()

    # ── Dominican Republic ────────────────────────────────
    if "santo domingo" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "La Bandera Dominicana", "subcategory": "Local Dish", "address": "Comedores throughout Santo Domingo, Dominican Republic", "description": "The iconic Dominican plate — rice, beans, and stewed meat. Best at a neighborhood comedor.", "vibe": "Authentic", "cost": "$", "transport": "Ask your hotel for the nearest comedor"},
                    {"name": "Mangú con Los Tres Golpes", "subcategory": "Breakfast", "address": "Local cafés, Zona Colonial, Santo Domingo", "description": "Mashed plantains with sautéed onions, fried cheese, salami, and eggs — a beloved Dominican breakfast.", "vibe": "Local favorite", "cost": "$", "transport": "Any local café"},
                    {"name": "Yaroa", "subcategory": "Street Food", "address": "Street vendors, Naco & Gazcue neighborhoods, Santo Domingo", "description": "Layered fries topped with meat, cheese, and sauces — the late-night street food of choice.", "vibe": "Late night", "cost": "$", "transport": "Street vendors near Naco/Gazcue at night"},
                    {"name": "Sancocho Dominicano", "subcategory": "Local Dish", "address": "Family restaurants, Gazcue, Santo Domingo", "description": "A hearty multi-meat stew with root vegetables and plantains — the ultimate Sunday comfort meal.", "vibe": "Traditional", "cost": "$", "transport": "Family restaurants in Gazcue"},
                    {"name": "Chicharrón de Pollo", "subcategory": "Street Food", "address": "Street stands, Mercado Modelo, Santo Domingo", "description": "Crispy marinated fried chicken chunks — the most popular street snack in the country.", "vibe": "Street staple", "cost": "$", "transport": "Near Mercado Modelo"},
                ],
                "drinks": [
                    {"name": "Mamajuana", "subcategory": "Local Spirit", "address": "Bars and restaurants, Zona Colonial, Santo Domingo", "description": "The DR's legendary herbal rum drink — rum, red wine, and honey soaked with tree bark. Every family has their own recipe.", "vibe": "Cultural", "cost": "$$", "transport": "Any bar in Zona Colonial"},
                    {"name": "Morir Soñando", "subcategory": "Local Drink", "address": "Juice stands, El Conde Street, Santo Domingo", "description": "Orange juice and evaporated milk blended together — sounds unusual, tastes incredible.", "vibe": "Refreshing", "cost": "$", "transport": "Juice stands on El Conde"},
                    {"name": "Presidente Beer", "subcategory": "Beer", "address": "Colmados and bars throughout Santo Domingo", "description": "The national beer — ice cold and best enjoyed at a neighborhood colmado.", "vibe": "Classic", "cost": "$", "transport": "Any colmado or bar"},
                ],
                "bars": [
                    {"name": "Malecón Sunset Strip", "subcategory": "Outdoor Bar", "address": "Av. George Washington (Malecón), Santo Domingo", "description": "Open-air bars line the waterfront boulevard — grab a Presidente and watch the Caribbean turn gold.", "vibe": "Lively", "cost": "$$", "transport": "Uber to Malecón (~10 min)"},
                    {"name": "Caña Bar", "subcategory": "Cocktail Bar", "address": "Calle Gustavo Mejía Ricart, Piantini, Santo Domingo", "description": "A popular craft cocktail bar in Piantini known for creative tropical drinks and a lively crowd.", "vibe": "Trendy", "cost": "$$", "transport": "Uber to Piantini"},
                    {"name": "Zona Colonial Rooftop Bars", "subcategory": "Rooftop", "address": "Calle El Conde & surroundings, Zona Colonial, Santo Domingo", "description": "Several rooftop bars in the colonial zone offer historic city views with cocktails and live music.", "vibe": "Upscale", "cost": "$$$", "transport": "Uber to Zona Colonial"},
                ],
                "restaurants": [
                    {"name": "Mesón de Bari", "subcategory": "Traditional Dominican", "address": "Calle Hostos 302, Zona Colonial, Santo Domingo", "description": "One of the most beloved traditional restaurants in the Zona Colonial. Authentic cuisine in a beautiful colonial setting.", "vibe": "Classic", "cost": "$$", "transport": "Uber to Zona Colonial"},
                    {"name": "Adrian Tropical", "subcategory": "Seafood", "address": "Av. George Washington, Malecón, Santo Domingo", "description": "A Santo Domingo institution on the Malecón — famous for fresh seafood, mofongo, and waterfront views.", "vibe": "Institution", "cost": "$$", "transport": "Uber to Malecón"},
                    {"name": "Jalao", "subcategory": "Modern Dominican", "address": "Calle Arzobispo Meriño 104, Zona Colonial, Santo Domingo", "description": "Modern Dominican cuisine in a beautifully designed colonial space. Great for a special dinner.", "vibe": "Upscale local", "cost": "$$$", "transport": "Uber to Zona Colonial"},
                    {"name": "El Conuco", "subcategory": "Traditional Dominican", "address": "Calle Casimiro de Moya 152, Gazcue, Santo Domingo", "description": "Live folkloric music and traditional Dominican food — food, music, and dance all in one place.", "vibe": "Cultural experience", "cost": "$$", "transport": "Uber to Gazcue"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Zona Colonial Walking Tour", "subcategory": "Cultural", "address": "Calle El Conde, Zona Colonial, Santo Domingo", "description": "Explore the oldest European city in the Americas on foot — cobblestone streets, the first cathedral in the New World.", "vibe": "Historic", "cost": "$", "transport": "Uber to Zona Colonial"},
                    {"name": "Cooking Class: Dominican Cuisine", "subcategory": "Cultural", "address": "Various studios, Gazcue, Santo Domingo", "description": "Learn to make mangú, sancocho, and tostones from a local cook. A hands-on cultural experience.", "vibe": "Cultural & fun", "cost": "$$", "transport": "Uber to Gazcue"},
                ],
                "beaches": [
                    {"name": "Playa Boca Chica", "subcategory": "Day Trip Beach", "address": "Boca Chica, Santo Domingo Este, Dominican Republic", "description": "The closest beach to Santo Domingo — calm shallow waters, beach bars, and weekend crowds.", "vibe": "Social", "cost": "$", "transport": "30 min drive east from Santo Domingo"},
                    {"name": "Playa Guayacanes", "subcategory": "Local Beach", "address": "Guayacanes, San Pedro de Macorís, Dominican Republic", "description": "A quieter alternative to Boca Chica — less crowded, more local atmosphere.", "vibe": "Relaxed", "cost": "Free", "transport": "45 min drive from Santo Domingo"},
                ],
                "landmarks": [
                    {"name": "Fortaleza Ozama", "subcategory": "Historic", "address": "Calle Las Damas, Zona Colonial, Santo Domingo", "description": "The oldest European fortress in the Americas, built in 1502. Climb the tower for river views.", "vibe": "Historic", "cost": "$", "transport": "Inside Zona Colonial — walk"},
                    {"name": "El Faro a Colón", "subcategory": "Monument", "address": "Av. España, Villa Duarte, Santo Domingo Este", "description": "A massive cross-shaped lighthouse built to honor Columbus. Architecturally stunning and historically significant.", "vibe": "Iconic", "cost": "$", "transport": "Uber (~15 min from center)"},
                    {"name": "Los Tres Ojos", "subcategory": "Natural Wonder", "address": "Av. Las Américas, Santo Domingo Este", "description": "Three underground lakes inside a limestone cave — a surreal natural wonder near the city.", "vibe": "Unique", "cost": "$", "transport": "Uber (~20 min)"},
                ],
                "experiences": [
                    {"name": "Bachata & Merengue Night", "subcategory": "Nightlife", "address": "Dance halls, Naco & Villa Mella, Santo Domingo", "description": "Merengue is the heartbeat of the DR. Find a local dance hall on Friday or Saturday — locals will teach you.", "vibe": "Cultural nightlife", "cost": "$$", "transport": "Uber to local venue"},
                    {"name": "Winter League Baseball Game", "subcategory": "Sports", "address": "Estadio Quisqueya, Av. Tiradentes, Santo Domingo", "description": "Baseball is a religion here. A Tigres del Licey vs. Águilas Cibaeñas game is loud, passionate, and unforgettable.", "vibe": "Authentic local", "cost": "$", "transport": "Uber to Estadio Quisqueya"},
                ]
            }
        }

    elif "punta cana" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "La Yola Restaurant", "subcategory": "Seafood", "address": "Marina Cap Cana, Punta Cana 23000, Dominican Republic", "description": "Built on stilts over the marina — fresh Caribbean seafood in a spectacular waterfront setting.", "vibe": "Upscale", "cost": "$$$", "transport": "Uber or resort shuttle to Cap Cana Marina"},
                    {"name": "Fresh Fish at El Cortecito", "subcategory": "Local Seafood", "address": "El Cortecito Beach, Bávaro, Punta Cana", "description": "Local fishermen sell their morning catch at this strip of casual beachside restaurants — as fresh as it gets.", "vibe": "Local", "cost": "$$", "transport": "Uber to El Cortecito (~15 min from most resorts)"},
                    {"name": "Tostones con Langosta", "subcategory": "Local Dish", "address": "Local restaurants, Bávaro, Punta Cana", "description": "Twice-fried plantains topped with fresh Caribbean lobster — a luxurious take on a Dominican classic.", "vibe": "Festive", "cost": "$$", "transport": "Local restaurants in Bávaro area"},
                ],
                "drinks": [
                    {"name": "Tropical Fruit Juice Bar", "subcategory": "Fresh Juice", "address": "El Cortecito Strip, Bávaro, Punta Cana", "description": "Fresh-squeezed passion fruit, tamarind, and guanábana juices made to order at beachside stands.", "vibe": "Refreshing", "cost": "$", "transport": "Walk along El Cortecito"},
                    {"name": "All-inclusive Beach Bar", "subcategory": "Cocktails", "address": "Bávaro Beach, Punta Cana", "description": "Most resorts have swim-up bars on Bávaro Beach — tropical cocktails with your feet in the sand.", "vibe": "Resort life", "cost": "Included", "transport": "Walk from your resort"},
                ],
                "bars": [
                    {"name": "Coco Bongo Punta Cana", "subcategory": "Nightclub", "address": "Blvd. Turístico del Este, Punta Cana 23301, Dominican Republic", "description": "The legendary party venue — acrobats, live shows, themed nights, and non-stop music until sunrise.", "vibe": "Party", "cost": "$$$", "transport": "Resort shuttle or Uber"},
                    {"name": "Imagine Club", "subcategory": "Cave Nightclub", "address": "Arena Gorda, Punta Cana, Dominican Republic", "description": "A nightclub built inside a natural limestone cave — one of the most unique party venues in the world.", "vibe": "Unique", "cost": "$$", "transport": "Resort shuttle (ask your hotel)"},
                ],
                "restaurants": [
                    {"name": "Chez Mon Ami", "subcategory": "French-Caribbean", "address": "Rincón Francés, Punta Cana", "description": "A charming French-Caribbean bistro in a quiet corner of the tourist strip — great for a romantic dinner.", "vibe": "Romantic", "cost": "$$$", "transport": "Uber from resort (~20 min)"},
                    {"name": "Bávaro Beach Club", "subcategory": "Casual Dining", "address": "Bávaro Beach, Punta Cana", "description": "Feet-in-the-sand dining with fresh grilled fish, lobster, and cocktails right on the famous beach.", "vibe": "Beachside", "cost": "$$", "transport": "Walk from Bávaro resorts"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Catamaran Snorkel & Sail", "subcategory": "Water", "address": "Bávaro Marina, Punta Cana, Dominican Republic", "description": "Sail the Caribbean on a catamaran with snorkeling stops at coral reefs, open bar, and live music.", "vibe": "Festive", "cost": "$$$", "transport": "Departs from Bávaro Marina — hotel shuttle available"},
                    {"name": "ATV Jungle Adventure", "subcategory": "Adventure", "address": "Excursión Bávaro, Punta Cana, Dominican Republic", "description": "Off-road ATV tours through jungle trails, sugarcane fields, and local villages — a Punta Cana classic.", "vibe": "Adventurous", "cost": "$$", "transport": "Hotel tour desk or Viator pickup"},
                    {"name": "Scape Park at Cap Cana", "subcategory": "Adventure Park", "address": "Cap Cana, Punta Cana 23000, Dominican Republic", "description": "A massive adventure park with zip lines, cenotes, horseback riding, and a water park all in one.", "vibe": "Adventure", "cost": "$$$", "transport": "Uber or shuttle to Cap Cana"},
                ],
                "beaches": [
                    {"name": "Bávaro Beach", "subcategory": "Resort Beach", "address": "Bávaro, Punta Cana, Dominican Republic", "description": "The postcard-perfect Caribbean beach — 32km of white sand and turquoise water. Best early morning.", "vibe": "Classic Caribbean", "cost": "Free", "transport": "Walk from resorts"},
                    {"name": "Playa Macao", "subcategory": "Wild Beach", "address": "Macao, Higüey, La Altagracia, Dominican Republic", "description": "An undeveloped beach with strong waves — popular with surfers escaping the resort strip.", "vibe": "Raw & natural", "cost": "Free", "transport": "Rental car or moto-taxi (~25 min from Bávaro)"},
                    {"name": "Playa Juanillo", "subcategory": "Secluded Beach", "address": "Cap Cana, Punta Cana, Dominican Republic", "description": "An upscale, uncrowded beach within Cap Cana — crystal clear water with no resort crowds.", "vibe": "Exclusive", "cost": "$$", "transport": "Uber to Cap Cana (~15 min)"},
                ],
                "landmarks": [
                    {"name": "Indigenous Eyes Ecological Park", "subcategory": "Nature Reserve", "address": "Puntacana Resort & Club, Punta Cana, Dominican Republic", "description": "A nature reserve with 12 freshwater lagoons, exotic birds, and tropical forest — a hidden gem near the resort strip.", "vibe": "Nature", "cost": "$$", "transport": "Inside Puntacana Resort — Uber or taxi"},
                    {"name": "Altos de Chavón", "subcategory": "Cultural Village", "address": "Altos de Chavón, La Romana, Dominican Republic", "description": "A recreated 16th-century Mediterranean village overlooking the Chavón River — home to galleries, restaurants, and a 5,000-seat amphitheater.", "vibe": "Artistic", "cost": "$", "transport": "1 hour drive from Punta Cana"},
                ],
                "experiences": [
                    {"name": "Swimming with Dolphins", "subcategory": "Animal Experience", "address": "Manati Park, Bávaro, Punta Cana, Dominican Republic", "description": "Interact with dolphins, manatees, and tropical wildlife at the famous Manati Park nature complex.", "vibe": "Unique", "cost": "$$$", "transport": "Uber or tour shuttle (~20 min)"},
                    {"name": "Dominican Cigar Factory Tour", "subcategory": "Cultural", "address": "Cigar shops, Punta Cana Village, Dominican Republic", "description": "Watch master cigar rollers at work and learn about the DR's world-famous tobacco industry.", "vibe": "Cultural", "cost": "$$", "transport": "Tour operator pickup from hotel"},
                ]
            }
        }

    elif "san juan" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Mofongo at La Bombonera", "subcategory": "Local Dish", "address": "Calle San Francisco 259, Old San Juan, Puerto Rico 00901", "description": "A Puerto Rican institution since 1902. Their mofongo — mashed plantains with garlic and pork — is legendary.", "vibe": "Iconic", "cost": "$$", "transport": "Walk in Old San Juan"},
                    {"name": "Alcapurrias at La Placita", "subcategory": "Street Food", "address": "Plaza Salvador Brau (La Placita), Santurce, Puerto Rico", "description": "Deep-fried fritters stuffed with crab or meat — the best street snack in Santurce on a Friday night.", "vibe": "Street food", "cost": "$", "transport": "Uber to Santurce (~10 min)"},
                    {"name": "Lechón Asado", "subcategory": "Local Dish", "address": "La Ruta del Lechón, Guavate, Cayey, Puerto Rico", "description": "Whole roasted pork — Puerto Rico's most beloved meal. Drive to Guavate for the real roadside experience.", "vibe": "Authentic", "cost": "$$", "transport": "1.5 hour drive south from San Juan"},
                ],
                "drinks": [
                    {"name": "Piña Colada at Barrachina", "subcategory": "Cocktail", "address": "Calle Fortaleza 104, Old San Juan, Puerto Rico 00901", "description": "Old San Juan's most famous bar claims to be the birthplace of the Piña Colada. Whether true or not, it's excellent.", "vibe": "Classic", "cost": "$$", "transport": "Walk in Old San Juan"},
                    {"name": "Don Q Rum Tasting", "subcategory": "Local Spirit", "address": "Various bars, Old San Juan, Puerto Rico", "description": "Puerto Rico is the rum capital of the world. Don Q is the local favorite — try it neat or in a classic cocktail.", "vibe": "Cultural", "cost": "$$", "transport": "Any bar in Old San Juan"},
                    {"name": "Medalla Light Beer", "subcategory": "Beer", "address": "Colmados and beach bars throughout San Juan, Puerto Rico", "description": "Puerto Rico's beloved light beer — ice cold, goes perfectly with the Caribbean heat.", "vibe": "Local", "cost": "$", "transport": "Any bar or colmado"},
                ],
                "bars": [
                    {"name": "La Factoría", "subcategory": "Cocktail Bar", "address": "Calle San Sebastián 148, Old San Juan, Puerto Rico 00901", "description": "Award-winning cocktail bar with multiple rooms, each with a different vibe. The best cocktails in Puerto Rico.", "vibe": "World-class", "cost": "$$", "transport": "Walk in Old San Juan"},
                    {"name": "La Placita de Santurce", "subcategory": "Bar District", "address": "Plaza Salvador Brau, Santurce, San Juan, Puerto Rico", "description": "A small plaza that explodes into an open-air street party on Thursday-Sunday nights. Locals, tourists, cold beers.", "vibe": "Street party", "cost": "$", "transport": "Uber to Santurce"},
                    {"name": "El Batey", "subcategory": "Dive Bar", "address": "Calle Cristo 101, Old San Juan, Puerto Rico 00901", "description": "A legendary, covered-in-graffiti dive bar in Old San Juan — cash only, strong drinks, real characters.", "vibe": "Legendary dive", "cost": "$", "transport": "Walk in Old San Juan"},
                ],
                "restaurants": [
                    {"name": "Marmalade Restaurant", "subcategory": "Fine Dining", "address": "Calle Fortaleza 317, Old San Juan, Puerto Rico 00901", "description": "One of the finest dining experiences in the Caribbean — creative tasting menus with Puerto Rican ingredients.", "vibe": "Fine dining", "cost": "$$$", "transport": "Walk in Old San Juan"},
                    {"name": "Raíces Restaurant", "subcategory": "Traditional Puerto Rican", "address": "Calle Recinto Sur 315, Old San Juan, Puerto Rico 00901", "description": "Traditional Puerto Rican comfort food in a colorful colonial space — mofongo, pernil, and arroz con gandules.", "vibe": "Traditional", "cost": "$$", "transport": "Walk in Old San Juan"},
                    {"name": "Lote 23", "subcategory": "Food Truck Park", "address": "Calle Loíza 2450, Miramar, San Juan, Puerto Rico 00913", "description": "A hip outdoor food park with the best local food trucks in San Juan — creative PR street food at its finest.", "vibe": "Trendy local", "cost": "$$", "transport": "Uber to Miramar (~10 min)"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Old San Juan Walking Tour", "subcategory": "Cultural", "address": "Calle El Morro, Old San Juan, Puerto Rico 00901", "description": "Walk the cobblestone streets of the 500-year-old walled city — cathedrals, plazas, forts, and colorful colonial houses.", "vibe": "Historic", "cost": "Free", "transport": "Free trolley or walk"},
                    {"name": "Kayaking in Laguna Grande", "subcategory": "Nature", "address": "Las Croabas, Fajardo, Puerto Rico 00738", "description": "Paddle through a bioluminescent bay at night — the water glows bright blue when disturbed. A magical experience.", "vibe": "Once in a lifetime", "cost": "$$", "transport": "1 hour drive from San Juan (tour pickup available)"},
                ],
                "beaches": [
                    {"name": "Condado Beach", "subcategory": "City Beach", "address": "Av. Ashford, Condado, San Juan, Puerto Rico", "description": "San Juan's most popular beach — right in the hotel strip, great waves, lined with restaurants and bars.", "vibe": "Lively", "cost": "Free", "transport": "Uber to Condado"},
                    {"name": "Ocean Park Beach", "subcategory": "Local Beach", "address": "Ocean Park, San Juan, Puerto Rico 00911", "description": "A calmer, more local alternative to Condado — less crowded, favored by surfers and families.", "vibe": "Local", "cost": "Free", "transport": "Uber to Ocean Park"},
                    {"name": "Flamenco Beach, Culebra", "subcategory": "Paradise Beach", "address": "Playa Flamenco, Culebra, Puerto Rico 00775", "description": "Consistently ranked one of the best beaches in the world — pristine white sand and crystal Caribbean water.", "vibe": "Paradise", "cost": "$$ (ferry)", "transport": "Ferry from Fajardo (~1 hr) or flight from SJU"},
                ],
                "landmarks": [
                    {"name": "Castillo San Felipe del Morro", "subcategory": "Historic Fort", "address": "Calle Norzagaray, Old San Juan, Puerto Rico 00901", "description": "The iconic 16th-century fortress that guards San Juan Bay. UNESCO World Heritage Site with stunning ocean views.", "vibe": "Historic & scenic", "cost": "$", "transport": "Walk from Old San Juan or Uber"},
                    {"name": "El Yunque Rainforest", "subcategory": "National Forest", "address": "Route 191, Río Grande, Puerto Rico 00745", "description": "The only tropical rainforest in the US National Forest System — waterfalls, hiking trails, and spectacular views.", "vibe": "Nature", "cost": "$$", "transport": "45 min drive from San Juan (rental car recommended)"},
                ],
                "experiences": [
                    {"name": "San Sebastián Street Festival", "subcategory": "Festival", "address": "Calle San Sebastián, Old San Juan, Puerto Rico", "description": "If visiting in January — the most famous street festival in the Caribbean, with live music, food, and dancing.", "vibe": "Festive", "cost": "Free", "transport": "Walk in Old San Juan"},
                    {"name": "Rum Distillery Tour", "subcategory": "Cultural", "address": "Casa Bacardí, Cataño, Puerto Rico 00962", "description": "Tour the world's largest rum distillery just across the bay from Old San Juan via ferry.", "vibe": "Cultural", "cost": "$$", "transport": "Ferry to Cataño ($0.50) then short taxi"},
                ]
            }
        }

    elif "cartagena" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Arepas de Chócolo", "subcategory": "Street Food", "address": "Street vendors, Centro Histórico, Cartagena, Colombia", "description": "Sweet corn arepas topped with cheese and butter — a beloved Colombian street snack at every corner.", "vibe": "Local", "cost": "$", "transport": "Walk in the Walled City"},
                    {"name": "Ceviche de Camarón", "subcategory": "Seafood", "address": "La Boquilla Beach, Cartagena, Colombia", "description": "Fresh shrimp ceviche with lime, cilantro, and aji at beachside spots — the best way to eat in this coastal city.", "vibe": "Fresh & coastal", "cost": "$$", "transport": "Uber or boat to La Boquilla"},
                    {"name": "Bandeja Paisa", "subcategory": "Local Dish", "address": "Restaurants in Getsemaní, Cartagena, Colombia", "description": "Colombia's most iconic dish — a massive plate of beans, rice, pork belly, egg, avocado, and arepa.", "vibe": "Traditional", "cost": "$$", "transport": "Walk to Getsemaní"},
                ],
                "drinks": [
                    {"name": "Aguardiente Antioqueño", "subcategory": "Local Spirit", "address": "Bars, Calle del Arsenal, Getsemaní, Cartagena", "description": "Colombia's anise-flavored spirit — the go-to at every party. Shots are shared with strangers here.", "vibe": "Social", "cost": "$", "transport": "Walk to Getsemaní"},
                    {"name": "Corozo Juice", "subcategory": "Local Drink", "address": "Juice stands, Plaza de los Coches, Cartagena, Colombia", "description": "Bright red juice from the native corozo palm fruit — tart, refreshing, and uniquely Cartagenera.", "vibe": "Local favorite", "cost": "$", "transport": "Walk to Plaza de los Coches"},
                ],
                "bars": [
                    {"name": "Café del Mar", "subcategory": "Rooftop Bar", "address": "Baluarte de Santo Domingo, Centro Histórico, Cartagena, Colombia", "description": "A bar built on top of the ancient city walls — sunset cocktails with the entire Caribbean stretching before you.", "vibe": "Iconic sunset", "cost": "$$$", "transport": "Walk to city walls"},
                    {"name": "Bazurto Social Club", "subcategory": "Live Music Bar", "address": "Calle de la Media Luna 10-46, Getsemaní, Cartagena, Colombia", "description": "The best live champeta and cumbia in Cartagena — a local crowd, real music, and dancing until dawn.", "vibe": "Authentic nightlife", "cost": "$$", "transport": "Walk to Getsemaní"},
                ],
                "restaurants": [
                    {"name": "La Cevichería", "subcategory": "Seafood", "address": "Calle Stuart 7-14, Centro Histórico, Cartagena, Colombia", "description": "Made famous by Anthony Bourdain — creative ceviches and fresh seafood in a simple but beloved colonial space.", "vibe": "Famous & delicious", "cost": "$$", "transport": "Walk in Walled City"},
                    {"name": "El Santísimo", "subcategory": "Modern Colombian", "address": "Calle del Torno 39-76, San Diego, Cartagena, Colombia", "description": "Contemporary Colombian cuisine in a beautiful colonial house — one of Cartagena's top dining experiences.", "vibe": "Upscale", "cost": "$$$", "transport": "Walk in San Diego"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Walled City Walking Tour", "subcategory": "Cultural", "address": "Centro Histórico, Cartagena, Colombia", "description": "Walk the 400-year-old walls and cobblestone streets of one of the best-preserved colonial cities in the Americas.", "vibe": "Historic", "cost": "Free", "transport": "Walk — entire center is on foot"},
                    {"name": "Day Trip to Islas del Rosario", "subcategory": "Island Excursion", "address": "Muelle de los Pegasos, Cartagena, Colombia", "description": "A boat trip to the coral archipelago 45 min offshore — snorkeling, swimming, and pristine Caribbean waters.", "vibe": "Paradise", "cost": "$$", "transport": "Boat from Muelle de los Pegasos"},
                ],
                "beaches": [
                    {"name": "Playa Blanca, Barú", "subcategory": "Day Trip Beach", "address": "Barú Island, Bolívar, Colombia", "description": "A postcard-white sand beach 2 hours from Cartagena — one of the most beautiful beaches in Colombia.", "vibe": "Stunning", "cost": "$$", "transport": "Boat tour or bus+boat from Cartagena"},
                    {"name": "La Boquilla Beach", "subcategory": "Local Beach", "address": "La Boquilla, Cartagena, Colombia", "description": "A local fishing village beach on a narrow strip between the sea and a lagoon — authentic and uncrowded.", "vibe": "Local", "cost": "Free", "transport": "Uber (~15 min from center)"},
                ],
                "landmarks": [
                    {"name": "Castillo San Felipe de Barajas", "subcategory": "Historic Fort", "address": "Cra. 17, San Lázaro, Cartagena, Colombia", "description": "The largest Spanish fortification built in the Americas — an architectural marvel with incredible city views.", "vibe": "Historic", "cost": "$", "transport": "Walk or Uber from Walled City"},
                    {"name": "Convento de la Popa", "subcategory": "Historic Site", "address": "Cerro de la Popa, Cartagena, Colombia", "description": "A 17th-century convent atop Cartagena's highest hill — 360-degree views of the city, bay, and islands.", "vibe": "Scenic & historic", "cost": "$", "transport": "Uber or tuk-tuk (~10 min)"},
                ],
                "experiences": [
                    {"name": "Palenque Village Visit", "subcategory": "Cultural", "address": "San Basilio de Palenque, Bolívar, Colombia", "description": "Visit the first free African town in the Americas — a UNESCO World Heritage community 1 hour from Cartagena.", "vibe": "Deeply cultural", "cost": "$$", "transport": "Guided tour from Cartagena"},
                    {"name": "Horse Carriage Ride", "subcategory": "Scenic", "address": "Centro Histórico, Cartagena, Colombia", "description": "A classic Cartagena experience — clip-clop through the colonial streets in a horse-drawn carriage at dusk.", "vibe": "Romantic", "cost": "$$", "transport": "Available at Plaza de Bolívar"},
                ]
            }
        }

    elif "medellín" in city_lower or "medellin" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Bandeja Paisa at El Rancho", "subcategory": "Local Dish", "address": "Calle 10 #43D-12, El Poblado, Medellín, Colombia", "description": "The definitive Colombian dish done right in Medellín — beans, rice, chicharrón, egg, and plantain on one plate.", "vibe": "Traditional", "cost": "$$", "transport": "Walk in El Poblado"},
                    {"name": "Empanadas at the Market", "subcategory": "Street Food", "address": "Plaza Minorista José María Villa, La América, Medellín", "description": "Medellín's best empanadas — crispy corn pockets filled with potato and meat, sold by the dozen.", "vibe": "Street staple", "cost": "$", "transport": "Uber to La América (~15 min)"},
                    {"name": "Ajiaco Soup", "subcategory": "Local Dish", "address": "Traditional restaurants, Laureles, Medellín, Colombia", "description": "A hearty Colombian chicken and potato soup with guasca herbs — the go-to comfort food on cool mountain evenings.", "vibe": "Comforting", "cost": "$", "transport": "Uber to Laureles"},
                ],
                "drinks": [
                    {"name": "Aguardiente at Parque El Poblado", "subcategory": "Local Spirit", "address": "Parque El Poblado, Calle 8A, El Poblado, Medellín", "description": "Sit at an outdoor table in Parque El Poblado with a bottle of aguardiente — the most Colombian evening possible.", "vibe": "Social", "cost": "$", "transport": "Walk in El Poblado"},
                    {"name": "Tinto (Colombian Coffee)", "subcategory": "Coffee", "address": "Café Pergamino, Cra. 37 #8A-37, El Poblado, Medellín", "description": "A small, sweet black coffee — the Colombian ritual. Café Pergamino serves some of the best specialty coffee in the country.", "vibe": "Local ritual", "cost": "$", "transport": "Walk in El Poblado"},
                ],
                "bars": [
                    {"name": "El Poblado Bar Scene", "subcategory": "Bar District", "address": "Parque El Poblado & Calle 9, El Poblado, Medellín, Colombia", "description": "El Poblado's streets come alive every night with dozens of bars, terrace restaurants, and clubs — the city's social hub.", "vibe": "Lively", "cost": "$$", "transport": "Walk in El Poblado"},
                    {"name": "Envy Rooftop Bar", "subcategory": "Rooftop", "address": "Calle 9 #38-20, El Poblado, Medellín, Colombia", "description": "A rooftop bar with sweeping views of Medellín's glowing valley at night — cocktails and the city at your feet.", "vibe": "Scenic", "cost": "$$", "transport": "Walk in El Poblado"},
                ],
                "restaurants": [
                    {"name": "Carmen Restaurant", "subcategory": "Modern Colombian", "address": "Calle 33A #7-46, El Poblado, Medellín, Colombia", "description": "One of Medellín's best restaurants — Colombian ingredients interpreted through a modern fine-dining lens.", "vibe": "Fine dining", "cost": "$$$", "transport": "Uber to El Poblado"},
                    {"name": "Hacienda Restaurante", "subcategory": "Traditional", "address": "Cra. 43A #19A Sur-30, El Poblado, Medellín, Colombia", "description": "Traditional paisa cooking in a beautiful hacienda setting — the complete Medellín culinary experience.", "vibe": "Traditional", "cost": "$$", "transport": "Uber to El Poblado"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Pablo Escobar Tour", "subcategory": "Historical Tour", "address": "Tours depart from El Poblado, Medellín, Colombia", "description": "A controversial but historically important tour of Escobar-related sites — best taken with local guides for full context.", "vibe": "Historical", "cost": "$$", "transport": "Tour pickup from El Poblado"},
                    {"name": "Graffiti Art Tour, Comuna 13", "subcategory": "Cultural", "address": "Comuna 13, San Javier, Medellín, Colombia", "description": "Walk the outdoor escalators and alleyways of the transformed neighborhood covered in world-class street art.", "vibe": "Transformative", "cost": "$", "transport": "Metro to San Javier station"},
                ],
                "beaches": [
                    {"name": "Guatapé Reservoir", "subcategory": "Lake Destination", "address": "Guatapé, Antioquia, Colombia (2 hours from Medellín)", "description": "Not a beach, but the best day trip from Medellín — a stunning reservoir with colorful towns and the iconic El Peñol rock.", "vibe": "Scenic escape", "cost": "$$", "transport": "Bus from Terminal del Norte (~2 hrs)"},
                ],
                "landmarks": [
                    {"name": "El Peñol Rock (La Piedra)", "subcategory": "Natural Landmark", "address": "El Peñol, Guatapé, Antioquia, Colombia", "description": "Climb 740 steps up a massive granite monolith for 360-degree views of the emerald Guatapé reservoir.", "vibe": "Spectacular", "cost": "$", "transport": "Bus from Medellín (~2 hrs)"},
                    {"name": "Plaza Botero", "subcategory": "Cultural Square", "address": "Cra. 52 #52-03, Centro, Medellín, Colombia", "description": "An outdoor museum showcasing 23 bronze sculptures by Fernando Botero — free to enjoy in the city center.", "vibe": "Cultural", "cost": "Free", "transport": "Metro to Parque Berrío"},
                ],
                "experiences": [
                    {"name": "Metro Cable Ride", "subcategory": "Scenic", "address": "Metro Acevedo Station, Aranjuez, Medellín, Colombia", "description": "Ride the cable car over the hillside comunas for stunning aerial views of the entire Medellín valley.", "vibe": "Unique", "cost": "$", "transport": "Metro to Acevedo station"},
                    {"name": "Feria de las Flores", "subcategory": "Festival", "address": "Centro de Medellín, Colombia", "description": "If visiting in August — Colombia's most famous flower festival with the iconic Silletero parade through the city streets.", "vibe": "Festive", "cost": "Free", "transport": "Metro to center"},
                ]
            }
        }

    elif "mexico city" in city_lower or "ciudad de méxico" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Tacos al Pastor at El Huequito", "subcategory": "Street Food", "address": "Calle Bolívar 58, Centro Histórico, Mexico City, Mexico", "description": "Mexico City's legendary taco — thin marinated pork shaved from a spinning trompo, topped with pineapple and cilantro.", "vibe": "Iconic", "cost": "$", "transport": "Walk in Centro Histórico"},
                    {"name": "Tamales at Mercado de Medellín", "subcategory": "Local Dish", "address": "Calle Campeche 101, Colonia Roma, Mexico City, Mexico", "description": "Freshly steamed tamales at this beloved Roma market — corn dough filled with mole, cheese, or rajas.", "vibe": "Traditional", "cost": "$", "transport": "Walk in Roma"},
                    {"name": "Tlayudas at Mercado Jamaica", "subcategory": "Street Food", "address": "Av. Congreso de la Unión 87, Venustiano Carranza, Mexico City", "description": "Oaxacan-style giant tortillas topped with beans, asiento, and your choice of protein — filling and delicious.", "vibe": "Street staple", "cost": "$", "transport": "Uber to Mercado Jamaica"},
                ],
                "drinks": [
                    {"name": "Mezcal at Mezcalería", "subcategory": "Local Spirit", "address": "Calle Tonalá 23, Colonia Roma, Mexico City, Mexico", "description": "Sip artisanal mezcal neat, the proper Mexican way — smoky, complex, and best with an orange slice and worm salt.", "vibe": "Artisanal", "cost": "$$", "transport": "Walk in Roma"},
                    {"name": "Horchata Fresca", "subcategory": "Local Drink", "address": "Juice stands and taquerías throughout Mexico City", "description": "Cold rice-almond milk sweetened with cinnamon and vanilla — the perfect counterpart to spicy tacos.", "vibe": "Refreshing", "cost": "$", "transport": "Any taquería or market"},
                    {"name": "Pulque at La Hija de los Apaches", "subcategory": "Traditional Drink", "address": "Calle Laredo 4, Colonia Guerrero, Mexico City, Mexico", "description": "A fermented agave drink that predates tequila by thousands of years — milky, slightly sour, uniquely Mexican.", "vibe": "Ancient local", "cost": "$", "transport": "Uber to Guerrero"},
                ],
                "bars": [
                    {"name": "Cantina El Pajaritos", "subcategory": "Traditional Cantina", "address": "Calle Mesones 79, Centro Histórico, Mexico City, Mexico", "description": "A classic Mexico City cantina with complimentary botanas — traditional drinking culture at its finest.", "vibe": "Traditional", "cost": "$", "transport": "Walk in Centro Histórico"},
                    {"name": "MALEA Bar", "subcategory": "Rooftop Bar", "address": "Av. Álvaro Obregón 25, Colonia Roma, Mexico City, Mexico", "description": "A stunning Roma rooftop bar with skyline views, creative cocktails, and a lively young crowd.", "vibe": "Trendy", "cost": "$$", "transport": "Walk in Roma"},
                ],
                "restaurants": [
                    {"name": "Pujol", "subcategory": "Fine Dining", "address": "Calle Tennyson 133, Polanco, Mexico City, Mexico", "description": "One of the world's top restaurants — Chef Enrique Olvera's reinterpretation of Mexican cuisine. Book weeks ahead.", "vibe": "World-class", "cost": "$$$", "transport": "Uber to Polanco"},
                    {"name": "Contramar", "subcategory": "Seafood", "address": "Calle Durango 200, Colonia Roma, Mexico City, Mexico", "description": "The most famous seafood restaurant in Mexico City — the tuna tostadas and grilled fish are life-changing.", "vibe": "Institution", "cost": "$$", "transport": "Walk in Roma"},
                    {"name": "Mercado de Coyoacán", "subcategory": "Market Food", "address": "Ignacio Allende s/n, Coyoacán, Mexico City, Mexico", "description": "A colorful market in the bohemian Coyoacán neighborhood — tostadas, quesadillas, and mole at market stalls.", "vibe": "Local & lively", "cost": "$", "transport": "Metro to Viveros + walk"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Lucha Libre Wrestling Match", "subcategory": "Entertainment", "address": "Arena México, Calle Dr. Lavista 197, Doctores, Mexico City", "description": "The most Mexican night out possible — masked wrestlers, acrobatic moves, passionate crowds, and pure spectacle.", "vibe": "Unmissable", "cost": "$", "transport": "Uber to Arena México"},
                    {"name": "Xochimilco Trajinera Boat Ride", "subcategory": "Cultural", "address": "Embarcadero Nuevo Nativitas, Xochimilco, Mexico City", "description": "Float through ancient Aztec canals on a colorful flat-bottomed boat with mariachi, food vendors, and other boats.", "vibe": "Festive & unique", "cost": "$$", "transport": "Metro to Tasqueña + tren ligero to Xochimilco"},
                ],
                "beaches": [
                    {"name": "Day Trip to Tulum Beaches", "subcategory": "Day Trip", "address": "Tulum, Quintana Roo, Mexico (1.5 hr flight)", "description": "Mexico City is landlocked, but Tulum is just a short flight away — turquoise Caribbean waters and Mayan ruins.", "vibe": "Escape", "cost": "$$$", "transport": "Flight from AICM (~1.5 hrs) or 4-hr ADO bus from TAPO"},
                ],
                "landmarks": [
                    {"name": "Teotihuacán Pyramids", "subcategory": "Ancient Ruins", "address": "Zona Arqueológica de Teotihuacán, San Juan Teotihuacán, Mexico", "description": "Climb the Pyramid of the Sun — one of the largest pyramids ever built. The ancient city of the gods, 45 min from CDMX.", "vibe": "Awe-inspiring", "cost": "$", "transport": "Bus from Terminal del Norte (~45 min)"},
                    {"name": "Museo Frida Kahlo (Casa Azul)", "subcategory": "Museum", "address": "Calle Londres 247, Coyoacán, Mexico City, Mexico", "description": "The iconic blue house where Frida Kahlo was born and died — her art, personal artifacts, and life on display.", "vibe": "Iconic", "cost": "$$", "transport": "Uber to Coyoacán (~30 min)"},
                    {"name": "Palacio de Bellas Artes", "subcategory": "Cultural Landmark", "address": "Av. Juárez s/n, Centro Histórico, Mexico City, Mexico", "description": "Mexico's most stunning building — Art Nouveau exterior, Diego Rivera murals inside, and world-class performances.", "vibe": "Grand", "cost": "Free (exterior)", "transport": "Walk from Centro Histórico"},
                ],
                "experiences": [
                    {"name": "Sunday Cycling on Paseo de la Reforma", "subcategory": "Active", "address": "Paseo de la Reforma, Mexico City, Mexico", "description": "Every Sunday, Mexico City's main boulevard closes to cars and opens to cyclists — join thousands of locals on bikes.", "vibe": "Local ritual", "cost": "Free", "transport": "Metro to Chapultepec"},
                    {"name": "Ballet Folklórico de México", "subcategory": "Cultural Performance", "address": "Palacio de Bellas Artes, Centro Histórico, Mexico City", "description": "A breathtaking performance of Mexico's traditional dances from all regions — costumes, music, and choreography at the highest level.", "vibe": "Cultural masterpiece", "cost": "$$", "transport": "Walk in Centro"},
                ]
            }
        }

    elif "cancún" in city_lower or "cancun" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Cochinita Pibil Tacos", "subcategory": "Local Dish", "address": "El Oasis Market, Av. Yaxchilán, Downtown Cancún, Mexico", "description": "Yucatecan slow-roasted pork wrapped in banana leaves — the region's most beloved dish, best at a downtown market.", "vibe": "Authentic Yucatecan", "cost": "$", "transport": "Uber to Downtown Cancún (~15 min from hotel zone)"},
                    {"name": "Sopa de Lima", "subcategory": "Local Dish", "address": "Traditional restaurants, Downtown Cancún, Mexico", "description": "A Yucatecan chicken-lime soup with crispy tortilla strips — the regional comfort food and a must-try.", "vibe": "Traditional", "cost": "$", "transport": "Uber to Downtown"},
                    {"name": "Mariscos (Fresh Seafood)", "subcategory": "Seafood", "address": "Mercado 28, Cancún Centro, Mexico", "description": "The best fresh seafood in Cancún is at local markets — ceviche, shrimp cocktails, and grilled fish away from tourist prices.", "vibe": "Local", "cost": "$", "transport": "Uber to Mercado 28"},
                ],
                "drinks": [
                    {"name": "Michelada", "subcategory": "Beer Cocktail", "address": "Beach bars throughout Cancún Hotel Zone, Mexico", "description": "Beer mixed with lime, hot sauce, and chili salt — Mexico's legendary spicy beer cocktail, perfect beach-side.", "vibe": "Beach staple", "cost": "$", "transport": "Any beach bar on the hotel strip"},
                    {"name": "Xtabentún Liqueur", "subcategory": "Local Spirit", "address": "Liquor shops, Downtown Cancún, Mexico", "description": "A traditional Yucatecan liqueur made from anise and fermented honey — sweet and unique to this region.", "vibe": "Local specialty", "cost": "$$", "transport": "Any local liquor shop"},
                ],
                "bars": [
                    {"name": "Coco Bongo Cancún", "subcategory": "Nightclub", "address": "Blvd. Kukulcán Km 9.5, Zona Hotelera, Cancún, Mexico", "description": "The most famous nightclub in Mexico — acrobats, live music, themed shows, and 5,000 people on the dance floor.", "vibe": "Party", "cost": "$$$", "transport": "Walk from hotel zone"},
                    {"name": "Mandala Beach Club", "subcategory": "Beach Club", "address": "Blvd. Kukulcán Km 9.5, Zona Hotelera, Cancún, Mexico", "description": "A daytime beach club that transforms into a full nightclub after dark — the full Cancún day-to-night experience.", "vibe": "Day-to-night", "cost": "$$", "transport": "Walk or R1 bus on hotel strip"},
                ],
                "restaurants": [
                    {"name": "La Habichuela", "subcategory": "Yucatecan", "address": "Calle Margaritas 25, Downtown Cancún, Mexico", "description": "A Cancún institution for over 40 years — authentic Mayan and Caribbean cuisine in a beautiful garden setting.", "vibe": "Classic", "cost": "$$", "transport": "Uber to Downtown Cancún"},
                    {"name": "Harry's Cancún", "subcategory": "Steakhouse/Seafood", "address": "Blvd. Kukulcán Km 14.2, Zona Hotelera, Cancún, Mexico", "description": "The best steak and seafood in the hotel zone — upscale but worth it for a special evening.", "vibe": "Upscale", "cost": "$$$", "transport": "Walk or Uber in hotel zone"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Snorkeling at MUSA Underwater Museum", "subcategory": "Unique Attraction", "address": "Isla Mujeres waters, off Cancún, Mexico", "description": "Snorkel or dive through 500 life-size sculptures installed on the ocean floor — a surreal and unforgettable experience.", "vibe": "Unique", "cost": "$$", "transport": "Boat tour from Cancún marina"},
                    {"name": "Day Trip to Chichén Itzá", "subcategory": "Ruins", "address": "Chichén Itzá, Yucatán, Mexico", "description": "One of the New Seven Wonders of the World — the magnificent Mayan pyramid El Castillo, 2 hours from Cancún.", "vibe": "Unmissable", "cost": "$$", "transport": "ADO bus or tour from hotel zone"},
                ],
                "beaches": [
                    {"name": "Playa Delfines (Beach 90)", "subcategory": "Public Beach", "address": "Blvd. Kukulcán Km 20, Zona Hotelera, Cancún, Mexico", "description": "The most beautiful public beach in the hotel zone — less crowded, stunning turquoise water, and the famous Cancún sign.", "vibe": "Beautiful & free", "cost": "Free", "transport": "R1/R2 bus or Uber in hotel zone"},
                    {"name": "Isla Mujeres Beach", "subcategory": "Island Beach", "address": "Playa Norte, Isla Mujeres, Quintana Roo, Mexico", "description": "A short ferry from Cancún leads to one of the most beautiful beaches in Mexico — calm clear water and a relaxed island vibe.", "vibe": "Island escape", "cost": "$ (ferry)", "transport": "Ferry from Puerto Juárez (~30 min)"},
                ],
                "landmarks": [
                    {"name": "El Meco Archaeological Zone", "subcategory": "Ruins", "address": "Carr. Puerto Juárez, Cancún, Mexico", "description": "A small but impressive Mayan site just outside Cancún — often overlooked, but well-preserved and crowd-free.", "vibe": "Hidden gem", "cost": "$", "transport": "Uber from hotel zone (~20 min)"},
                    {"name": "Chichén Itzá", "subcategory": "UNESCO World Heritage", "address": "Chichén Itzá, Yucatán, Mexico", "description": "The most famous Mayan ruins in the world and a New 7 Wonder — get there early to beat the heat and crowds.", "vibe": "Iconic", "cost": "$$", "transport": "ADO bus (~3 hrs) or private tour"},
                ],
                "experiences": [
                    {"name": "Cenote Ik-Kil Swim", "subcategory": "Nature", "address": "Cenote Ik-Kil, near Chichén Itzá, Yucatán, Mexico", "description": "Swim in a sacred Mayan sinkhole — 26 meters deep, surrounded by hanging vines and waterfalls.", "vibe": "Magical", "cost": "$$", "transport": "Combine with Chichén Itzá tour"},
                    {"name": "Holbox Island Day Trip", "subcategory": "Island Escape", "address": "Holbox, Quintana Roo, Mexico", "description": "A remote, car-free island 2.5 hours from Cancún — bioluminescent waters, whale sharks (seasonal), and pure tranquility.", "vibe": "Off the beaten path", "cost": "$$", "transport": "ADO bus to Chiquilá + ferry (~2.5 hrs total)"},
                ]
            }
        }

    elif "tulum" in city_lower:
        return {
            "gastronomy": {
                "food": [
                    {"name": "Tacos at El Camello Jr.", "subcategory": "Street Food", "address": "Av. Tulum, Tulum Pueblo, Quintana Roo, Mexico", "description": "The best fish and shrimp tacos in Tulum — a local institution in the town center far from the beach club prices.", "vibe": "Local value", "cost": "$", "transport": "Walk or bike in Tulum town"},
                    {"name": "Cochinita Pibil Breakfast", "subcategory": "Local Dish", "address": "Market stalls, Tulum Pueblo, Quintana Roo, Mexico", "description": "Slow-roasted Yucatecan pork on handmade tortillas — best eaten as breakfast at a local market stall.", "vibe": "Authentic", "cost": "$", "transport": "Bike to Tulum town"},
                ],
                "drinks": [
                    {"name": "Natural Wine at Arca", "subcategory": "Wine Bar", "address": "Carretera Tulum-Boca Paila Km 7.5, Tulum Beach, Mexico", "description": "One of Tulum's top beach restaurants with a stunning natural wine list and organic cuisine.", "vibe": "Upscale bohemian", "cost": "$$$", "transport": "Bike or scooter to beach zone"},
                    {"name": "Fresh Coco Loco", "subcategory": "Cocktail", "address": "Beach clubs, Tulum Beach Zone, Quintana Roo, Mexico", "description": "Fresh coconut water mixed with rum and a squeeze of lime — the quintessential Tulum beach drink.", "vibe": "Beachy", "cost": "$$", "transport": "Any beach club on Tulum beach road"},
                ],
                "bars": [
                    {"name": "Papaya Playa Project", "subcategory": "Beach Club/Bar", "address": "Carretera Tulum-Boca Paila Km 4.5, Tulum, Mexico", "description": "A legendary beach club with full moon parties and excellent DJs — the social center of Tulum nightlife.", "vibe": "Bohemian party", "cost": "$$$", "transport": "Bike or scooter to beach zone"},
                    {"name": "Batey Mojito & Guarapo Bar", "subcategory": "Bar", "address": "Av. Satellite, Tulum Pueblo, Quintana Roo, Mexico", "description": "A casual town bar known for the freshest mojitos in Tulum — made with hand-pressed sugarcane juice.", "vibe": "Local hangout", "cost": "$", "transport": "Walk or bike in Tulum town"},
                ],
                "restaurants": [
                    {"name": "Hartwood", "subcategory": "Farm-to-Table", "address": "Carretera Tulum-Boca Paila Km 7.6, Tulum, Mexico", "description": "James Beard-nominated restaurant cooking over live fire with local ingredients — no reservations, arrive early.", "vibe": "World-class", "cost": "$$$", "transport": "Bike or scooter to beach road"},
                    {"name": "El Asadero", "subcategory": "Mexican Grill", "address": "Calle Beta, Tulum Pueblo, Quintana Roo, Mexico", "description": "A beloved local grill spot in town with incredible tacos and grilled meats at non-beach-club prices.", "vibe": "Local value", "cost": "$", "transport": "Walk in Tulum town"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": "Cenote Dos Ojos Snorkel/Dive", "subcategory": "Nature", "address": "Cenote Dos Ojos, Carretera Tulum-Cobá Km 10, Tulum", "description": "One of the longest underwater cave systems in the world — crystal clear fresh water in an eerie, beautiful cavern.", "vibe": "Breathtaking", "cost": "$$", "transport": "Bike or scooter (~20 min from Tulum)"},
                    {"name": "Coba Ruins Bike to Pyramid", "subcategory": "Adventure", "address": "Zona Arqueológica de Cobá, Cobá, Quintana Roo, Mexico", "description": "Rent a bike through the jungle to reach Cobá's towering pyramid — still climbable and far fewer crowds than Chichén Itzá.", "vibe": "Adventure", "cost": "$", "transport": "Rental car or colectivo (~45 min from Tulum)"},
                ],
                "beaches": [
                    {"name": "Playa Paraíso", "subcategory": "Beach", "address": "Zona Hotelera de Tulum, Quintana Roo, Mexico", "description": "The most photographed beach in Tulum — powdery white sand, turquoise water, and the Mayan ruins on the cliff above.", "vibe": "Iconic", "cost": "Free (access)", "transport": "Bike or scooter along the beach road"},
                    {"name": "Sian Ka'an Biosphere", "subcategory": "Nature Reserve", "address": "Sian Ka'an Biosphere Reserve, Quintana Roo, Mexico", "description": "A UNESCO World Heritage nature reserve — boat through mangroves, swim in cenotes, and spot exotic wildlife.", "vibe": "Pure nature", "cost": "$$", "transport": "Tour from Tulum (~1 hr south)"},
                ],
                "landmarks": [
                    {"name": "Tulum Mayan Ruins", "subcategory": "Archaeological Site", "address": "Zona Arqueológica Tulum, Av. Sol Oriente, Tulum, Mexico", "description": "Mayan ruins perched on a Caribbean cliff — the most dramatically located ruins in Mexico. Arrive at opening time.", "vibe": "Iconic", "cost": "$", "transport": "Walk from town or bike"},
                    {"name": "Gran Cenote", "subcategory": "Natural Wonder", "address": "Carretera Tulum-Cobá Km 3, Tulum, Quintana Roo, Mexico", "description": "One of the most beautiful cenotes in Mexico — swimming through stalactite caves into open pools of crystal water.", "vibe": "Magical", "cost": "$", "transport": "Bike or scooter (~10 min from town)"},
                ],
                "experiences": [
                    {"name": "Yoga at Sunrise on the Beach", "subcategory": "Wellness", "address": "Various beach clubs and cenotes, Tulum Beach, Mexico", "description": "Tulum is the yoga capital of Mexico — morning classes on platforms over the jungle or directly on the sand.", "vibe": "Spiritual", "cost": "$$", "transport": "Bike to beach zone"},
                    {"name": "Full Moon Beach Party", "subcategory": "Nightlife", "address": "Papaya Playa Project, Tulum Beach Zone, Mexico", "description": "Monthly full moon parties on the beach — bonfires, live electronic music, and the Caribbean glowing in moonlight.", "vibe": "Festive", "cost": "$$$", "transport": "Scooter to beach zone"},
                ]
            }
        }

    else:
        # Generic fallback for any city not explicitly handled
        # Still uses the city name so it's better than always showing DR
        return {
            "gastronomy": {
                "food": [
                    {"name": f"Local Market in {city}", "subcategory": "Street Food", "address": f"Central Market, {city}, {destination}", "description": f"The best local flavors are found at {city}'s central market — fresh ingredients, traditional recipes, and real local life.", "vibe": "Authentic", "cost": "$", "transport": "Ask your hotel for the nearest market"},
                    {"name": f"Traditional Dish of {destination}", "subcategory": "Local Dish", "address": f"Traditional restaurants, {city}, {destination}", "description": f"Ask locals for their favorite spot to try the signature dish of {destination} — every city has its version of the classic.", "vibe": "Traditional", "cost": "$$", "transport": "Ask hotel for a recommendation"},
                ],
                "drinks": [
                    {"name": f"Local Juice Bar", "subcategory": "Fresh Juice", "address": f"Market area, {city}, {destination}", "description": f"Fresh tropical juices made from local fruit — a refreshing way to start the morning in {city}.", "vibe": "Refreshing", "cost": "$", "transport": "Any market or street stand"},
                    {"name": f"Local Craft Beer", "subcategory": "Beer", "address": f"Bars throughout {city}, {destination}", "description": f"Try the local craft or regional beer — every Latin American city has its own brewery culture.", "vibe": "Local", "cost": "$", "transport": "Any local bar"},
                ],
                "bars": [
                    {"name": f"Historic District Bar Scene", "subcategory": "Bar District", "address": f"Historic center, {city}, {destination}", "description": f"The historic center of {city} typically has the best concentration of bars, cafés, and nightlife spots.", "vibe": "Lively", "cost": "$$", "transport": "Walk in city center"},
                ],
                "restaurants": [
                    {"name": f"Top-rated Local Restaurant", "subcategory": "Traditional", "address": f"City center, {city}, {destination}", "description": f"Ask your hotel or Airbnb host for their personal recommendation — locals always know the best spots that don't show up online.", "vibe": "Authentic", "cost": "$$", "transport": "Ask your accommodation"},
                ]
            },
            "activities": {
                "activities": [
                    {"name": f"City Walking Tour of {city}", "subcategory": "Cultural", "address": f"City center, {city}, {destination}", "description": f"The best way to discover {city} is on foot — explore the historic center, local neighborhoods, and hidden plazas.", "vibe": "Exploratory", "cost": "$", "transport": "Walk from your accommodation"},
                ],
                "beaches": [
                    {"name": f"Nearest Beach to {city}", "subcategory": "Beach", "address": f"Coastal area near {city}, {destination}", "description": f"Check with locals for the best nearby beach — most coastal cities in Latin America have stunning options within reach.", "vibe": "Relaxing", "cost": "Free-$$", "transport": "Ask hotel for transport options"},
                ],
                "landmarks": [
                    {"name": f"Historic Center of {city}", "subcategory": "Historic District", "address": f"Centro Histórico, {city}, {destination}", "description": f"Every city in Latin America and the Caribbean has a historic center worth exploring — colonial architecture, churches, and plazas.", "vibe": "Historic", "cost": "Free", "transport": "Walk or short Uber ride"},
                ],
                "experiences": [
                    {"name": f"Local Music & Dance Night", "subcategory": "Cultural Nightlife", "address": f"Live music venues, {city}, {destination}", "description": f"Latin America is alive with music — find a local venue with live cumbia, salsa, merengue, or whatever the region dances to.", "vibe": "Cultural", "cost": "$$", "transport": "Ask hotel for best venues"},
                ]
            }
        }


async def generate_itinerary(
    destination: str,
    city: str,
    check_in: str,
    check_out: str,
    group_type: str,
    budget: str,
    vibes: list,
    accommodation: str,
    weather: list
) -> dict:
    """Generate curated recommendations using OpenAI or city-specific mock data."""

    transport = TRANSPORT_INFO.get(city, {
        "options": ["Uber (widely available)", "Local taxis", "Walking"],
        "tip": "Uber is available in most major cities. Ask your hotel for local transport advice."
    })

    if not os.getenv("OPENAI_API_KEY"):
        city_data = get_mock_for_city(city, destination)
        city_data["transport"] = transport
        city_data["city"] = city
        city_data["destination"] = destination
        city_data["group_type"] = group_type
        city_data["budget"] = budget
        city_data["vibes"] = vibes
        city_data["weather"] = weather
        city_data["tips"] = _get_tips_for_city(city, destination)
        return city_data

    vibe_str = ", ".join(vibes) if vibes else "general sightseeing"
    weather_note = ""
    if weather:
        sunny_days = sum(1 for w in weather if w.get("is_sunny"))
        rainy_days = len(weather) - sunny_days
        weather_note = f"{sunny_days} sunny days, {rainy_days} rainy days forecast."

    prompt = f"""You are Wayo, an expert local guide for Latin America and the Caribbean.

Generate curated local recommendations for a traveler visiting {city}, {destination}.

TRIP DETAILS:
- Destination: {city}, {destination}
- Dates: {check_in} to {check_out}
- Group type: {group_type}
- Budget level: {budget}
- Interests: {vibe_str}
- Staying near: {accommodation if accommodation else "city center"}
- Weather: {weather_note}

Generate 8-10 recommendations for EACH of these 8 subcategories:
1. food — local dishes and street food
2. drinks — local beverages, juices, spirits
3. bars — bars, nightlife spots, lounges
4. restaurants — sit-down dining spots
5. activities — things to do, tours, adventures
6. beaches — beaches and waterfront spots (if landlocked city, include best day trip options)
7. landmarks — historic sites, viewpoints, iconic places
8. experiences — cultural events, music, sports, unique local experiences

RULES:
- Use REAL, SPECIFIC place names, street names, and neighborhoods for {city}, {destination}
- Include full address (street address, neighborhood, city, country) for every recommendation
- Tailor all content specifically to {city} — do NOT use generic or placeholder descriptions
- Be authentic — local spots over tourist traps
- Each recommendation must have: name, subcategory, address, description (2 sentences), vibe tag, cost ($/$$/$$$ ), transport note

Return ONLY valid JSON in this exact format:
{{
  "city": "{city}",
  "destination": "{destination}",
  "group_type": "{group_type}",
  "budget": "{budget}",
  "gastronomy": {{
    "food": [
      {{"name": "...", "subcategory": "Local Dish|Street Food|Snack", "address": "Street, Neighborhood, {city}, {destination}", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "drinks": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "bars": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "restaurants": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ]
  }},
  "activities": {{
    "activities": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "beaches": [
      {{"name": "...", "subcategory": "Beach", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "landmarks": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ],
    "experiences": [
      {{"name": "...", "subcategory": "...", "address": "...", "description": "...", "vibe": "...", "cost": "$|$$|$$$", "transport": "..."}}
    ]
  }},
  "transport": {{
    "options": {json.dumps(transport['options'])},
    "tip": "{transport['tip']}"
  }},
  "tips": ["tip1", "tip2", "tip3", "tip4"]
}}"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=6000
        )
        result = json.loads(response.choices[0].message.content)
        result["weather"] = weather
        return result
    except Exception as e:
        # City-specific fallback instead of always showing DR data
        city_data = get_mock_for_city(city, destination)
        city_data["transport"] = transport
        city_data["city"] = city
        city_data["destination"] = destination
        city_data["group_type"] = group_type
        city_data["budget"] = budget
        city_data["vibes"] = vibes
        city_data["weather"] = weather
        city_data["tips"] = _get_tips_for_city(city, destination)
        city_data["error"] = str(e)
        return city_data


def _get_tips_for_city(city: str, destination: str) -> list:
    city_lower = city.lower()
    if "santo domingo" in city_lower or "punta cana" in city_lower or "santiago" in city_lower:
        return [
            "Always carry small bills in pesos — street vendors and colmados rarely give change",
            "Download Uber before arriving — it's the safest and most reliable transport",
            "Learn a few Spanish phrases — locals deeply appreciate the effort",
            "Avoid drinking tap water — stick to bottled water throughout the DR",
            "Bargain respectfully at local markets — it's part of the culture",
            "Try the street food — chicharrón de pollo and pastelitos are safe and delicious"
        ]
    elif "san juan" in city_lower or "ponce" in city_lower:
        return [
            "Puerto Rico uses the US dollar — no currency exchange needed",
            "Old San Juan is completely walkable — wear comfortable shoes",
            "Rent a car for day trips to El Yunque and the bioluminescent bays",
            "Beaches are public by law in Puerto Rico — no private beach access",
            "Try a piragua (shaved ice) from a street cart on a hot day",
            "Cell service works normally — US carriers work without roaming fees"
        ]
    elif "cartagena" in city_lower:
        return [
            "Stay inside the Walled City or Getsemaní for the best experience",
            "Take tuk-tuks for short trips — they're cheap and fit through the narrow streets",
            "Negotiate prices before getting into a horse carriage",
            "Book Islas del Rosario day trips through reputable operators only",
            "The heat is intense — plan outdoor activities for morning or evening",
            "Learn basic Spanish — English is limited outside tourist zones"
        ]
    elif "medellín" in city_lower or "medellin" in city_lower:
        return [
            "Medellín has a spring climate year-round — pack a light jacket for evenings",
            "The Metro is safe, clean, and covers most tourist areas",
            "El Poblado is the safest and most tourist-friendly neighborhood",
            "Visit Comuna 13 with a local guide for full historical context",
            "Book the Guatapé day trip early — it's the best day trip from the city",
            "Altitude is around 1,500m — take it easy on the first day if you're sensitive"
        ]
    elif "mexico city" in city_lower:
        return [
            "Mexico City sits at 2,240m altitude — drink extra water and rest on day one",
            "The Metro is the fastest and cheapest way to get around",
            "Roma, Condesa, and Polanco are the safest and liveliest neighborhoods",
            "Always use Uber or Cabify — never hail taxis off the street",
            "Eat street tacos fearlessly — they're safe and absolutely delicious",
            "Book Pujol and other top restaurants weeks in advance"
        ]
    elif "cancún" in city_lower or "cancun" in city_lower:
        return [
            "The hotel zone (Zona Hotelera) is for resorts — downtown has the real local life",
            "R1/R2 buses run the full hotel strip for $0.60 — no Uber needed on the strip",
            "Visit Chichén Itzá as early as possible — gates open at 8am, heat is brutal by noon",
            "Swim in cenotes — they're the freshwater wonder of the Yucatán",
            "The Caribbean currents can be strong — check beach flags before swimming",
            "Negotiate taxi prices before getting in — flat rates are standard"
        ]
    elif "tulum" in city_lower:
        return [
            "Rent a bike or scooter — town and beach zone are 3km apart and you'll ride constantly",
            "Arrive at Tulum ruins at 8am opening — it's packed and hot by 10am",
            "Bring cash — many cenotes and small restaurants are cash only",
            "Beach club minimum spends can be $50+ — know what you're signing up for",
            "Protect cenotes — biodegradable sunscreen is required at most, don't apply chemical SPF",
            "Town is far cheaper than the beach strip for food and drinks"
        ]
    else:
        return [
            f"Always carry some local currency for street food and small vendors in {city}",
            "Download Uber before arriving — it's available in most Latin American cities",
            "Learn a few Spanish phrases — locals always appreciate the effort",
            "Avoid drinking tap water — stick to bottled water",
            "Bargain respectfully at local markets — it's often expected",
            f"Ask your hotel or host for their personal restaurant recommendations in {city}"
        ]
