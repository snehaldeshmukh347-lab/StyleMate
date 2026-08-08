import os
import json
import copy

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OPENAI_API_KEY")

# The app can run with OpenAI or fallback smart generative engine
client = OpenAI(api_key=API_KEY) if API_KEY and API_KEY.startswith("sk-") else None


# =========================================================
# SHOPPING SEARCH LINKS GENERATOR
# =========================================================

def shopping_links(item_name, style="", audience="Women", kids_age=""):
    if not item_name or str(item_name).lower() in ["none", "n/a", "not applicable"]:
        return {}

    aud_lower = str(audience).lower()
    item_str = str(item_name).strip()

    if "kid" in aud_lower or "child" in aud_lower:
        age_str = str(kids_age).lower()
        if "toddler" in age_str or "2–4" in age_str or "2-4" in age_str:
            prefix = "toddler"
        elif "little" in age_str or "5–8" in age_str or "5-8" in age_str:
            prefix = "kids"
        elif "pre-teen" in age_str or "9–12" in age_str or "9-12" in age_str:
            prefix = "pre teen"
        elif "teen" in age_str or "13–16" in age_str or "13-16" in age_str:
            prefix = "teen"
        else:
            prefix = "kids"

        # Remove adult terms if present
        for adult_kw in ["women's blazer", "women blazer", "women heels", "women handbag", "adult dress", "men's formalwear", "women", "woman", "adult", "ladies"]:
            item_str = item_str.replace(adult_kw, "").replace(adult_kw.capitalize(), "").strip()

        # Prepend age prefix if not already starting with it
        if not item_str.lower().startswith(prefix):
            query = f"{prefix} {item_str}".strip()
        else:
            query = item_str.strip()
    else:
        query = f"{style} {item_str}".strip()

    query = " ".join(query.split())

    encoded_plus = query.replace(" ", "+")
    encoded_percent = query.replace(" ", "%20")
    encoded_dash = query.replace(" ", "-")

    return {
        "Amazon": f"https://www.amazon.in/s?k={encoded_plus}",
        "Myntra": f"https://www.myntra.com/{encoded_dash}",
        "AJIO": f"https://www.ajio.com/search/?text={encoded_percent}"
    }


# =========================================================
# FALLBACK STYLIST (SMART GENERATIVE ENGINE)
# Used when OpenAI API is unconfigured or unavailable
# =========================================================

def fallback_outfits(data):
    audience = str(data.get("audience", data.get("gender", "Women"))).lower()
    kids_age = str(data.get("kidsAge", "Toddler (2–4 yrs)"))
    style = str(data.get("style", "Western"))
    occasion = str(data.get("occasion", "Casual"))
    body_type = str(data.get("bodyType", "Hourglass"))
    skin_tone = str(data.get("skinTone", "Medium"))
    colors = data.get("colors", ["Black", "Beige"])
    if isinstance(colors, str):
        colors = [c.strip() for c in colors.split(",") if c.strip()]

    color_str = " · ".join(colors) if colors else "Black & Beige"
    occ_lower = occasion.lower()

    looks = []

    # HARD CONSTRAINT 1: KIDS / AGE GROUP (DYNAMIC BY AGE & KIDS OCCASION)
    if "kid" in audience or "child" in audience:
        if "birthday" in occ_lower:
            looks = [
                {
                    "id": "look_k_bday_1",
                    "name": "LOOK 01 · Birthday Star Outfit",
                    "description": f"Vibrant, party-ready celebration wear tailored for {kids_age}.",
                    "items": {
                        "top": f"Soft 100% cotton-lined {style.lower()} party tunic / shirt",
                        "bottom_or_dress": "Soft stretch waistband cotton tulle skirt / party trousers",
                        "shoes": "Cushioned non-slip metallic party shoes",
                        "outerwear": "Lightweight plush bolero jacket",
                        "accessories": "Glitter star birthday headband & matching socks",
                        "bag": "Mini velvet drawstring pouch",
                        "styling": "Cute bouncy hair curls with a shiny hair clip."
                    },
                    "colors": color_str,
                    "styling_tip": "Soft interior lining ensures zero itchy seams during birthday cake fun.",
                    "why_it_works": f"Curated specifically for a birthday celebration in the {kids_age} age group: combines festive sparkle with 100% skin comfort."
                },
                {
                    "id": "look_k_bday_2",
                    "name": "LOOK 02 · Charming Party Celebration",
                    "description": f"Elegant, comfortable party look suited for {kids_age}.",
                    "items": {
                        "top": "Breathable cotton satin embroidered party top",
                        "bottom_or_dress": "Elasticated chino party shorts / flared skirt",
                        "shoes": "Soft flexible leather slip-on shoes",
                        "outerwear": "None",
                        "accessories": "Gentle fabric bowtie / hair ribbon",
                        "bag": "Mini crossbody pouch",
                        "styling": "Clean neat hairdo with soft styling gel."
                    },
                    "colors": "Pastel Pink · Cream · Gold",
                    "styling_tip": "Flexible waistband offers full freedom for games.",
                    "why_it_works": f"Provides playful party flair tailored specifically for {kids_age}."
                },
                {
                    "id": "look_k_bday_3",
                    "name": "LOOK 03 · Fun & Colourful Outfit",
                    "description": f"Playful, photo-friendly birthday outfit for {kids_age}.",
                    "items": {
                        "top": "Printed cotton party crewneck shirt",
                        "bottom_or_dress": "Soft denim dungarees / cotton tiered dress",
                        "shoes": "Lightweight retro canvas sneakers",
                        "outerwear": "Light denim jacket",
                        "accessories": "Colorful kids sunglasses & socks",
                        "bag": "Mini canvas backpack",
                        "styling": "High ponytail or neat comb-up."
                    },
                    "colors": "Sky Blue · Coral · Sunshine Yellow",
                    "styling_tip": "Durable stain-resistant cotton blend.",
                    "why_it_works": "Vibrant and easy to wash after cake and outdoor party activities."
                }
            ]

        elif "wedding" in occ_lower or "family" in occ_lower:
            looks = [
                {
                    "id": "look_k_wed_1",
                    "name": "LOOK 01 · Royal Mini Ethnic Outfit",
                    "description": f"Charming festive wedding ensemble for {kids_age} with soft interior lining.",
                    "items": {
                        "top": "Pure chanderi cotton-lined silk kurta top / blouse",
                        "bottom_or_dress": "Soft waist silk-blend dhoti pants / flared lehenga skirt",
                        "shoes": "Cushioned flexible-sole metallic zari juttis",
                        "outerwear": "None",
                        "accessories": "Gentle floral wristband & velvet bindi",
                        "bag": "Handmade mini velvet potli pouch",
                        "styling": "Cute side braid with soft bow ribbon."
                    },
                    "colors": "Ruby Red · Warm Gold · Ivory",
                    "styling_tip": "100% skin-friendly interior lining.",
                    "why_it_works": f"Grand wedding elegance designed specifically for {kids_age} without scratchy tags or heavy weight."
                },
                {
                    "id": "look_k_wed_2",
                    "name": "LOOK 02 · Modern Mini Indo-Western",
                    "description": f"Flowy fusion festive outfit tailored for {kids_age}.",
                    "items": {
                        "top": "Embroidered cotton-silk jacket top",
                        "bottom_or_dress": "Elasticated dhoti trousers / layered skirt",
                        "shoes": "Soft metallic strap sandals",
                        "outerwear": "Sheer mirror-work cape layer",
                        "accessories": "Subtle hair clips & bracelet",
                        "bag": "Mini satin sling bag",
                        "styling": "Half-up half-down hairstyle."
                    },
                    "colors": "Dusty Rose · Gold · Champagne",
                    "styling_tip": "Cape layer stays in place effortlessly.",
                    "why_it_works": "Combines royal wedding aesthetics with lightweight child mobility."
                },
                {
                    "id": "look_k_wed_3",
                    "name": "LOOK 03 · Elegant Formal Suit / Dress",
                    "description": f"Sophisticated wedding party wear for {kids_age}.",
                    "items": {
                        "top": "Crisp cotton dress shirt / satin bodice top",
                        "bottom_or_dress": "Tailored elastic-waist suit trousers / satin midi dress",
                        "shoes": "Patent leather dress shoes / ballet flats",
                        "outerwear": "Soft velvet blazer jacket",
                        "accessories": "Satin bowtie / floral brooch",
                        "bag": "Mini velvet bag",
                        "styling": "Sleek combed hair."
                    },
                    "colors": "Midnight Navy · Ivory · Silver",
                    "styling_tip": "Unstructured shoulders for easy arm movement.",
                    "why_it_works": f"Tailored specifically for formal family functions in the {kids_age} category."
                }
            ]

        elif "school" in occ_lower or "study" in occ_lower or "campus" in occ_lower:
            looks = [
                {
                    "id": "look_k_sch_1",
                    "name": "LOOK 01 · Preppy Campus / School Outfit",
                    "description": f"Neat, breathable outfit curated for {kids_age} school & campus days.",
                    "items": {
                        "top": "Fine organic cotton pique polo shirt / rib knit top",
                        "bottom_or_dress": "Tailored stretch chino trousers / pleated denim skirt",
                        "shoes": "Cushioned white leather sneakers with crew socks",
                        "outerwear": "Lightweight varsity fleece cardigan",
                        "accessories": "Simple watch & hairband",
                        "bag": "Ergonomic lightweight canvas school backpack",
                        "styling": "Neat sleek ponytail / comb-up."
                    },
                    "colors": "Navy Blue · Cream · Heather Grey",
                    "styling_tip": "Breathable cotton keeps kids cool during study sessions.",
                    "why_it_works": f"For {kids_age}: clean campus aesthetic that meets school dress codes while offering all-day desk and playground comfort."
                },
                {
                    "id": "look_k_sch_2",
                    "name": "LOOK 02 · Casual Campus Streetwear",
                    "description": f"Trendy, comfortable campus look for {kids_age}.",
                    "items": {
                        "top": "Heavyweight cotton graphic crewneck tee",
                        "bottom_or_dress": "High-waisted relaxed stretch denim jeans",
                        "shoes": "Retro canvas high-top sneakers",
                        "outerwear": "Cropped denim overshirt",
                        "accessories": "Minimalist silver hoop earrings & cap",
                        "bag": "Canvas tote bag",
                        "styling": "Tousled natural hair with lip balm."
                    },
                    "colors": "Vintage Blue · White · Beige",
                    "styling_tip": "High waist denim allows comfortable seating.",
                    "why_it_works": f"Age-appropriate casual chic suited for {kids_age} campus outings."
                },
                {
                    "id": "look_k_sch_3",
                    "name": "LOOK 03 · Comfortable Layered Study Fit",
                    "description": f"Easy-wear layered fit for long study sessions.",
                    "items": {
                        "top": "Soft jersey cotton long-sleeve tee",
                        "bottom_or_dress": "Relaxed cotton twill cargo trousers",
                        "shoes": "Slip-on canvas shoes",
                        "outerwear": "Zip-up fleece jacket",
                        "accessories": "Beaded bracelet",
                        "bag": "Nylon crossbody sling bag",
                        "styling": "Casual low ponytail."
                    },
                    "colors": "Olive · Oatmeal · Navy",
                    "styling_tip": "Elastic waist for effortless comfort.",
                    "why_it_works": "Durable easy-care fabrics built for everyday school wear."
                }
            ]

        elif "festive" in occ_lower or "diwali" in occ_lower:
            looks = [
                {
                    "id": "look_k_fes_1",
                    "name": "LOOK 01 · Festive Silk Kurta Set",
                    "description": f"Vibrant festive Indian ensemble tailored for {kids_age}.",
                    "items": {
                        "top": "Straight-cut cotton silk embroidered kurta top",
                        "bottom_or_dress": "Matching soft silk palazzo trousers / churidar",
                        "shoes": "Cushioned embroidered metallic juttis",
                        "outerwear": "None",
                        "accessories": "Jhumka earrings / bindi & bangles",
                        "bag": "Raw silk embroidered potli pouch",
                        "styling": "Half-up half-down hairstyle with ribbons."
                    },
                    "colors": "Ruby Red · Warm Gold · Mustard",
                    "styling_tip": "Soft lining prevents skin rubbing.",
                    "why_it_works": f"Rich traditional Diwali silk colors tailored for {kids_age} skin comfort."
                },
                {
                    "id": "look_k_fes_2",
                    "name": "LOOK 02 · Modern Anarkali / Kurta Suit",
                    "description": f"Flared cotton-silk festive wear for {kids_age}.",
                    "items": {
                        "top": "Flared chanderi silk anarkali top",
                        "bottom_or_dress": "Soft cotton churidar bottoms",
                        "shoes": "Low block-heel / flat metallic sandals",
                        "outerwear": "None",
                        "accessories": "Chandbali earrings & bracelet",
                        "bag": "Hand-beaded clutch pouch",
                        "styling": "Soft braids with lip gloss."
                    },
                    "colors": "Dusty Rose · Gold · Champagne",
                    "styling_tip": "Flared length drape allows easy walking.",
                    "why_it_works": f"Royal festive movement built with lightweight fabrics for {kids_age}."
                },
                {
                    "id": "look_k_fes_3",
                    "name": "LOOK 03 · Indo-Western Fusion Set",
                    "description": f"Crop top paired with dhoti trousers and embroidered jacket for {kids_age}.",
                    "items": {
                        "top": "Silk embroidered bustier top",
                        "bottom_or_dress": "Pleated satin dhoti trousers",
                        "shoes": "Pointed metallic mules / flats",
                        "outerwear": "Mirror-work open jacket",
                        "accessories": "Oxidized silver necklace & rings",
                        "bag": "Embroidered sling pouch",
                        "styling": "Messy boho bun."
                    },
                    "colors": "Ivory · Teal · Silver",
                    "styling_tip": "Jacket adds festive sparkle without heavy weight.",
                    "why_it_works": "Modern fusion aesthetic popular for young family celebrations."
                }
            ]

        else:
            # Kids Everyday / Casual / Play / Vacation Default
            looks = [
                {
                    "id": "look_k_gen_1",
                    "name": f"LOOK 01 · Playful {style} Outfit",
                    "description": f"Comfortable, durable, tag-free outfit curated for {kids_age}.",
                    "items": {
                        "top": f"Soft breathable organic cotton crewneck tee in {color_str}",
                        "bottom_or_dress": "Elasticated soft-waist stretch denim jeans / skirt",
                        "shoes": "Cushioned non-slip velcro sneakers with ankle support",
                        "outerwear": "Lightweight fleece-lined zip hoodie",
                        "accessories": "Soft cotton sun cap & matching socks",
                        "bag": "Mini lightweight canvas backpack",
                        "styling": "Comfy comb-up hair, ready for active play."
                    },
                    "colors": color_str,
                    "styling_tip": "Soft stretch waist and zero scratchy tags.",
                    "why_it_works": f"Designed specifically for {kids_age}: 100% breathable cotton, scratch-free seams, durable for playground mobility."
                },
                {
                    "id": "look_k_gen_2",
                    "name": "LOOK 02 · Relaxed Weekend Outing",
                    "description": f"Easy-wash, stain-resistant casual wear for {kids_age}.",
                    "items": {
                        "top": "Breathable striped jersey cotton shirt",
                        "bottom_or_dress": "Stretch chino shorts / soft cotton leggings",
                        "shoes": "Lightweight canvas slip-on shoes",
                        "outerwear": "Light denim jacket",
                        "accessories": "UV-protection kids sunglasses",
                        "bag": "Small crossbody utility pouch",
                        "styling": "Clean casual neat hair look."
                    },
                    "colors": "Sky Blue · Cream · Tan",
                    "styling_tip": "Durable reinforced knee seams.",
                    "why_it_works": f"Stain-resistant fabric blend tailored specifically for energetic {kids_age} play."
                },
                {
                    "id": "look_k_gen_3",
                    "name": "LOOK 03 · Cozy Everyday Comfort",
                    "description": f"Ultra-soft casual ensemble for {kids_age}.",
                    "items": {
                        "top": "Fine rib-knit long-sleeve cotton top",
                        "bottom_or_dress": "Soft cotton jogger trousers",
                        "shoes": "Flexible sole running sneakers",
                        "outerwear": "Cropped cardigan",
                        "accessories": "Soft fabric headband",
                        "bag": "Mini canvas tote",
                        "styling": "Natural hair with a soft smile."
                    },
                    "colors": "Oatmeal · Pastel Pink · Heather Grey",
                    "styling_tip": "Machine washable premium cotton.",
                    "why_it_works": "Maximum softness for sensitive young skin."
                }
            ]

    # MEN OUTFITS
    elif audience in ["men", "male", "man"]:
        looks = [
            {
                "id": "look_m_1",
                "name": "LOOK 01 · Main Character Tailoring",
                "description": f"Sharp, effortless {style} ensemble for {occasion}.",
                "items": {
                    "top": "Linen-blend Cuban collar shirt in warm cream",
                    "bottom_or_dress": "Tailored flat-front slim chino trousers",
                    "shoes": "Italian suede penny loafers in tan leather",
                    "outerwear": "Unstructured lightweight cotton blazer",
                    "accessories": "Leather strap chronograph watch & tortoiseshell sunglasses",
                    "bag": "Structured leather folio document case",
                    "styling": "Neatly groomed hair with matte clay texture finish."
                },
                "colors": "Midnight Navy · Sand Beige · Ivory",
                "styling_tip": "Unstructured shoulders widen chest visually.",
                "why_it_works": f"For a {body_type} frame, the Cuban collar widens shoulder width visually while slim chinos maintain sleek leg proportions."
            },
            {
                "id": "look_m_2",
                "name": "LOOK 02 · Effortless Modern Casual",
                "description": "Layered urban silhouette combining comfort with clean structure.",
                "items": {
                    "top": "Heavyweight drop-shoulder organic cotton T-shirt",
                    "bottom_or_dress": "Relaxed-fit cotton twill cargo trousers",
                    "shoes": "Retro multi-panel white leather platform sneakers",
                    "outerwear": "Oversized utility overshirt in khaki",
                    "accessories": "Stainless steel curb chain & silver ring stack",
                    "bag": "Canvas utility crossbody bag",
                    "styling": "Clean low fade haircut with subtle matte wax styling."
                },
                "colors": "Charcoal Black · Olive Green · White",
                "styling_tip": "Boxy shoulders balance upper torso ratio.",
                "why_it_works": "Boxy drop shoulders balance midsection while relaxed cargos offer a contemporary streetwear taper."
            },
            {
                "id": "look_m_3",
                "name": "LOOK 03 · Trend Forward Elegance",
                "description": "High-fashion statement look with refined tailored lines.",
                "items": {
                    "top": "Crisp poplin spread-collar dress shirt",
                    "bottom_or_dress": "Tapered pleated wool-blend suit trousers",
                    "shoes": "Burnished calfskin Oxford dress shoes",
                    "outerwear": "Single-breasted wool blazer",
                    "accessories": "Patterned silk pocket square & calfskin belt",
                    "bag": "Leather weekend duffle bag",
                    "styling": "Classic side part pompadour hair style."
                },
                "colors": "Charcoal Grey · Pure White · Mahogany",
                "styling_tip": "Spread collar elongates neck line.",
                "why_it_works": "Unstructured shoulder padding conforms smoothly over chest line without feeling boxy."
            }
        ]

    # WOMEN OUTFITS (STRICT HARD CONSTRAINTS BY OCCASION)
    else:
        if "college" in occ_lower or "campus" in occ_lower or "school" in occ_lower:
            looks = [
                {
                    "id": "look_w_col_1",
                    "name": "LOOK 01 · Elevated Campus Chic",
                    "description": "Trendy wide-leg denim paired with a fitted rib knit top.",
                    "items": {
                        "top": "Fitted rib-knit square-neck top in cream",
                        "bottom_or_dress": "High-waisted wide-leg vintage blue jeans",
                        "shoes": "Retro platform white leather sneakers",
                        "outerwear": "Oversized cropped corduroy overshirt",
                        "accessories": "Minimalist gold hoop earrings & 90s oval sunglasses",
                        "bag": "Canvas tote bag with leather shoulder straps",
                        "styling": "Tousled natural waves with a dewy lip oil finish."
                    },
                    "colors": "Cream · Vintage Denim · Beige",
                    "styling_tip": "Tuck top into high waist jeans to define waistline.",
                    "why_it_works": f"For an {body_type} body shape and {skin_tone} skin tone, wide-leg denim elongates legs while a fitted square neck highlights shoulders."
                },
                {
                    "id": "look_w_col_2",
                    "name": "LOOK 02 · Effortless Layered Cool",
                    "description": "Relaxed pleated trousers with a cropped cardigan and sneakers.",
                    "items": {
                        "top": "Soft fine-knit cropped cardigan top",
                        "bottom_or_dress": "Tailored relaxed pleated beige trousers",
                        "shoes": "Minimalist leather dad sneakers",
                        "outerwear": "Lightweight denim trucker jacket",
                        "accessories": "Layered gold chain necklace & claw clip updos",
                        "bag": "Nylon everyday crossbody bag",
                        "styling": "Messy claw-clip updo with glossy lip gloss."
                    },
                    "colors": "Oatmeal · Beige · White",
                    "styling_tip": "High waist trousers create a sleek lengthen effect.",
                    "why_it_works": "Combines collegiate comfort with clean tailored lines appropriate for campus lectures and library study."
                },
                {
                    "id": "look_w_col_3",
                    "name": "LOOK 03 · Preppy Streetwear",
                    "description": "Pleated mini skirt or cargo trousers with a slouchy sweatshirt.",
                    "items": {
                        "top": "Oversized college graphic cotton sweatshirt",
                        "bottom_or_dress": "High-rise pleated mini skirt / beige cargo pants",
                        "shoes": "Chunky white retro sneakers with crew socks",
                        "outerwear": "None",
                        "accessories": "Baseball cap & mini hoop earrings",
                        "bag": "Minimalist leather shoulder bag",
                        "styling": "Sleek low ponytail with clean glow makeup."
                    },
                    "colors": "Heather Grey · Navy · White",
                    "styling_tip": "Pair oversized sweatshirt with fitted skirt for contrast ratio.",
                    "why_it_works": "Youthful, trend-forward college aesthetic that looks stylish without trying too hard."
                }
            ]

        elif "date" in occ_lower or "romantic" in occ_lower:
            looks = [
                {
                    "id": "look_w_date_1",
                    "name": "LOOK 01 · Champagne Silk Romance",
                    "description": "Refined bias-cut slip dress designed for romantic candlelit dinners.",
                    "items": {
                        "top": "None (One-Piece Slip Dress)",
                        "bottom_or_dress": "Bias-cut liquid satin midi slip dress in champagne gold",
                        "shoes": "Minimalist nude ankle-strap heeled sandals",
                        "outerwear": "None",
                        "accessories": "Sculpted gold drop earrings & delicate wrist chain",
                        "bag": "Structured hard-shell clutch bag",
                        "styling": "Soft romantic blowout waves with glossy nude lips."
                    },
                    "colors": "Champagne Gold · Nude · Warm Rose",
                    "styling_tip": "Bias cut drapes smoothly over hips.",
                    "why_it_works": f"Fluid satin bias drape highlights {body_type} curves gracefully while champagne gold flatters {skin_tone} undertones."
                },
                {
                    "id": "look_w_date_2",
                    "name": "LOOK 02 · Modern Elegant Two-Piece",
                    "description": "Satin corset top paired with high-waisted pleated midi skirt.",
                    "items": {
                        "top": "Cowl-neck satin drape corset top",
                        "bottom_or_dress": "High-waisted pleated A-line satin midi skirt",
                        "shoes": "Pointed-toe slingback heels",
                        "outerwear": "None",
                        "accessories": "Layered pearl pendant choker & crystal ring",
                        "bag": "Quilted mini leather shoulder bag",
                        "styling": "Sleek low chignon bun with warm blush."
                    },
                    "colors": "Black · Ivory · Rose Gold",
                    "styling_tip": "High waist midi skirt flatters natural waistline.",
                    "why_it_works": "Satin textures catch evening light while A-line cut provides comfortable movement."
                },
                {
                    "id": "look_w_date_3",
                    "name": "LOOK 03 · Sophisticated Chic Trousers",
                    "description": "Silk camisole layered with tailored trousers and heels.",
                    "items": {
                        "top": "Lace-trimmed silk camisole top",
                        "bottom_or_dress": "High-rise tailored wide-leg crepe trousers",
                        "shoes": "Strappy stiletto heels",
                        "outerwear": "Tailored structured blazer draped on shoulders",
                        "accessories": "Gold hoop earrings & delicate pendant necklace",
                        "bag": "Crossbody leather chain bag",
                        "styling": "Voluminous curls with berry lip tint."
                    },
                    "colors": "Onyx Black · Cream · Blush",
                    "styling_tip": "Draping blazer over shoulders adds effortless elegance.",
                    "why_it_works": "Sharp trouser tailoring balances feminine lace camisole for a modern date night silhouette."
                }
            ]

        elif "office" in occ_lower or "corporate" in occ_lower or "interview" in occ_lower:
            looks = [
                {
                    "id": "look_w_off_1",
                    "name": "LOOK 01 · Power Suiting Tailoring",
                    "description": "Polished blazer suit paired with a silk shell top and pumps.",
                    "items": {
                        "top": "Silk crewneck shell blouse in ivory",
                        "bottom_or_dress": "Tailored high-waisted straight-leg suit trousers",
                        "shoes": "Pointed-toe leather pumps / loafers",
                        "outerwear": "Single-breasted tailored wool-blend blazer",
                        "accessories": "Minimalist leather watch & stud earrings",
                        "bag": "Structured leather tote bag (laptop compatible)",
                        "styling": "Sleek low bun with clean corporate makeup."
                    },
                    "colors": "Taupe Beige · Ivory · Black",
                    "styling_tip": "Structured shoulder pads elongate stature.",
                    "why_it_works": f"For an {body_type} body type, sharp shoulder tailoring creates an authoritative, professional corporate presence."
                },
                {
                    "id": "look_w_off_2",
                    "name": "LOOK 02 · Modern Business Casual",
                    "description": "Fine-knit sweater layered with a pleated midi skirt or chinos.",
                    "items": {
                        "top": "Fine-gauge cashmere-blend turtleneck sweater",
                        "bottom_or_dress": "High-rise pleated A-line midi skirt / tailored chinos",
                        "shoes": "Burnished leather penny loafers",
                        "outerwear": "Belted trench coat",
                        "accessories": "Small gold hoop earrings & slim leather belt",
                        "bag": "Structured top-handle leather satchel",
                        "styling": "Neat blow-dry with warm neutral lip."
                    },
                    "colors": "Camel · Oatmeal · Espresso",
                    "styling_tip": "Tuck sweater into waistline for clean proportions.",
                    "why_it_works": "Soft knit texture maintains professional elegance while providing all-day office comfort."
                },
                {
                    "id": "look_w_off_3",
                    "name": "LOOK 03 · Executive Wrap Dress",
                    "description": "Tailored wrap dress with structured accessories.",
                    "items": {
                        "top": "None (One-Piece Wrap Dress)",
                        "bottom_or_dress": "Tailored knee-length crepe wrap dress in navy",
                        "shoes": "Low block-heel leather pumps",
                        "outerwear": "None",
                        "accessories": "Pearl stud earrings & leather wristband",
                        "bag": "Structured saffiano leather tote",
                        "styling": "Soft side-parted hair with subtle eyeliner."
                    },
                    "colors": "Midnight Navy · Nude · Gold",
                    "styling_tip": "V-neckline elongates neck visual height.",
                    "why_it_works": "Wrap silhouette highlights natural waist while maintaining modest corporate knee length."
                }
            ]

        elif "wedding" in occ_lower or "gala" in occ_lower or "reception" in occ_lower:
            looks = [
                {
                    "id": "look_w_wed_1",
                    "name": "LOOK 01 · Royal Champagne Organza Saree",
                    "description": "Opulent hand-embroidered organza saree with zari work blouse.",
                    "items": {
                        "top": "Embellished gold zardozi silk saree blouse",
                        "bottom_or_dress": "Pre-stitched hand-embroidered tissue organza saree in champagne gold",
                        "shoes": "Cushioned embroidered zari block-heel juttis",
                        "outerwear": "None",
                        "accessories": "Kundan chandelier earrings & pearl choker necklace",
                        "bag": "Handmade velvet embroidered potli bag",
                        "styling": "Sleek low bun with fresh white jasmine flowers & bold crimson lip."
                    },
                    "colors": "Champagne Gold · Ivory · Emerald",
                    "styling_tip": "Pleat pallu cleanly over shoulder to reveal waist embroidery.",
                    "why_it_works": f"Opulent gold zari embroidery complements {skin_tone} undertones and adds grand wedding elegance."
                },
                {
                    "id": "look_w_wed_2",
                    "name": "LOOK 02 · Modern Fusion Lehenga",
                    "description": "Silk lehenga skirt paired with a draped cape top.",
                    "items": {
                        "top": "Embellished silk bustier top with flowing sheer organza cape",
                        "bottom_or_dress": "High-waisted flared silk lehenga skirt",
                        "shoes": "Metallic ankle-strap heeled sandals",
                        "outerwear": "Sheer embroidered cape layer",
                        "accessories": "Statement polki choker & ring stack",
                        "bag": "Metallic box clutch",
                        "styling": "Voluminous curls with winged eyeliner."
                    },
                    "colors": "Rose Gold · Deep Plum · Bronze",
                    "styling_tip": "High waist lehenga highlights smallest waist section.",
                    "why_it_works": "Cape jacket adds regal movement without requiring a heavy dupatta."
                },
                {
                    "id": "look_w_wed_3",
                    "name": "LOOK 03 · Black-Tie Haute Couture Gown",
                    "description": "Floor-length satin evening gown with sculpted neckline.",
                    "items": {
                        "top": "None (One-Piece Evening Gown)",
                        "bottom_or_dress": "Floor-length sculpted satin corset gown with side leg slit",
                        "shoes": "Crystal-embellished stiletto heels",
                        "outerwear": "Faux-fur stole wrap",
                        "accessories": "Diamond-style drop earrings & tennis bracelet",
                        "bag": "Satin evening clutch",
                        "styling": "Hollywood glamour waves with classic red lip."
                    },
                    "colors": "Emerald Green · Diamond Silver · Onyx",
                    "styling_tip": "High slit offers leg length extension.",
                    "why_it_works": "Corset boning defines torso structure for formal gala events."
                }
            ]

        elif "festive" in occ_lower or "diwali" in occ_lower or "traditional" in occ_lower:
            looks = [
                {
                    "id": "look_w_fes_1",
                    "name": "LOOK 01 · Festive Silk Kurta Set",
                    "description": "Rich chanderi silk kurta set with woven organza dupatta.",
                    "items": {
                        "top": "Straight-cut silk embroidered kurta top",
                        "bottom_or_dress": "Matching silk palazzo trousers with zari borders",
                        "shoes": "Cushioned embroidered metallic juttis",
                        "outerwear": "None",
                        "accessories": "Jhumka earrings & green bindi",
                        "bag": "Raw silk embroidered potli pouch",
                        "styling": "Half-up half-down hairstyle with soft warm blush."
                    },
                    "colors": "Ruby Red · Warm Gold · Mustard",
                    "styling_tip": "Drape dupatta gracefully over one arm.",
                    "why_it_works": f"Rich traditional silk colors highlight {skin_tone} complexion for Diwali festivities."
                },
                {
                    "id": "look_w_fes_2",
                    "name": "LOOK 02 · Modern Anarkali Suite",
                    "description": "Floor-length flared cotton silk anarkali suit.",
                    "items": {
                        "top": "Flared chanderi silk anarkali top",
                        "bottom_or_dress": "Churidar bottoms",
                        "shoes": "Low block-heel metallic sandals",
                        "outerwear": "None",
                        "accessories": "Statement chandbali earrings & cuff bracelet",
                        "bag": "Hand-beaded clutch bag",
                        "styling": "Soft braids with glossy nudish lip."
                    },
                    "colors": "Dusty Rose · Champagne · Gold",
                    "styling_tip": "Anarkali flare conceals midsection comfortably.",
                    "why_it_works": "Flared floor length drape creates royal festive movement while allowing comfortable movement for family functions."
                },
                {
                    "id": "look_w_fes_3",
                    "name": "LOOK 03 · Indo-Western Fusion Set",
                    "description": "Crop top paired with dhoti trousers and embroidered jacket.",
                    "items": {
                        "top": "Silk embroidered bustier crop top",
                        "bottom_or_dress": "Pleated satin dhoti trousers",
                        "shoes": "Pointed metallic mules",
                        "outerwear": "Floor-length mirror-work jacket",
                        "accessories": "Layered oxidized silver necklace & rings",
                        "bag": "Embroidered sling pouch",
                        "styling": "Messy boho bun with defined eyes."
                    },
                    "colors": "Ivory · Teal · Oxidized Silver",
                    "styling_tip": "Long jacket elongates visual silhouette height.",
                    "why_it_works": "Fusion silhouette combines modern comfort with festive mirror-work details."
                }
            ]

        elif "party" in occ_lower or "club" in occ_lower or "night" in occ_lower:
            looks = [
                {
                    "id": "look_w_pty_1",
                    "name": "LOOK 01 · Sleek Satin Nightlife",
                    "description": "Corset satin dress with heels and statement clutch.",
                    "items": {
                        "top": "None (One-Piece Corset Dress)",
                        "bottom_or_dress": "Structured liquid satin corset mini/midi dress",
                        "shoes": "High-heeled metallic ankle-strap sandals",
                        "outerwear": "Tailored cropped leather biker jacket",
                        "accessories": "Rhinestone hoop earrings & silver cuff",
                        "bag": "Metallic box clutch",
                        "styling": "Sleek liquid straight hair with smoky eye makeup."
                    },
                    "colors": "Onyx Black · Metallic Silver · Champagne",
                    "styling_tip": "Corset boning defines waist silhouette.",
                    "why_it_works": "High fashion nightlife glam without any neon cliché."
                },
                {
                    "id": "look_w_pty_2",
                    "name": "LOOK 02 · Statement Top & Leather Pants",
                    "description": "Asymmetric metallic top paired with tailored leather pants.",
                    "items": {
                        "top": "Asymmetric cowl-neck metallic halter top",
                        "bottom_or_dress": "High-waisted straight-leg faux leather trousers",
                        "shoes": "Pointed-toe stiletto ankle boots",
                        "outerwear": "None",
                        "accessories": "Layered silver chain choker & ear cuffs",
                        "bag": "Quilted mini shoulder bag",
                        "styling": "High sleek ponytail with nude glossy lip."
                    },
                    "colors": "Charcoal · Gunmetal Silver · Black",
                    "styling_tip": "High waist leather pants elongate legs.",
                    "why_it_works": "Chic, edgy party aesthetic suitable for upscale lounges and dining."
                },
                {
                    "id": "look_w_pty_3",
                    "name": "LOOK 03 · Velvet Glamour Set",
                    "description": "Deep velvet wrap skirt set with sparkling accessories.",
                    "items": {
                        "top": "Deep V-neck velvet crop top",
                        "bottom_or_dress": "Matching ruched velvet midi skirt with leg slit",
                        "shoes": "Crystal-embellished strappy heels",
                        "outerwear": "None",
                        "accessories": "Crystal drop chandelier earrings",
                        "bag": "Hard-shell glitter clutch",
                        "styling": "Voluminous curls with deep berry lip."
                    },
                    "colors": "Plum Burgundy · Black · Silver",
                    "styling_tip": "Ruched skirt contours natural hip curvature.",
                    "why_it_works": "Luxurious velvet texture catches ambient evening lighting elegantly."
                }
            ]

        else:
            # Beach / Resort / Travel / Casual Default
            looks = [
                {
                    "id": "look_w_res_1",
                    "name": "LOOK 01 · Coastal Sunset Glamour",
                    "description": "Flowy silk linen slip dress made for golden hour breeze.",
                    "items": {
                        "top": "None (One-Piece Slip Dress)",
                        "bottom_or_dress": "Relaxed halter silk slip midi dress with side leg vent",
                        "shoes": "Minimal nude strappy block-heel sandals",
                        "outerwear": "None",
                        "accessories": "Sculpted gold hoops & layered pearl pendant choker",
                        "bag": "Woven raffia tote bag with leather straps",
                        "styling": "Loose beach waves, glowing bronzer, and glossy nude lip."
                    },
                    "colors": "Onyx Black · Champagne Gold · Beige",
                    "styling_tip": "Loose halter neckline elongates shoulders.",
                    "why_it_works": f"For an {body_type} silhouette and {skin_tone} skin tone, the halter neckline elongates shoulders while fluid silk drapes curves."
                },
                {
                    "id": "look_w_res_2",
                    "name": "LOOK 02 · Beach Club Linen Chic",
                    "description": "Satin cowl-neck top paired with high-waisted wide-leg linen trousers.",
                    "items": {
                        "top": "Terracotta satin cowl-neck backless crop top",
                        "bottom_or_dress": "High-waisted wide-leg natural linen trousers",
                        "shoes": "Woven espadrille platform sandals",
                        "outerwear": "Lightweight unlined linen shirt overlayer",
                        "accessories": "Tortoiseshell sunglasses & woven raffia hat",
                        "bag": "Woven straw beach tote",
                        "styling": "High sleek ponytail with warm coral blush."
                    },
                    "colors": "Terracotta · Cream White · Gold",
                    "styling_tip": "High-waisted wide-leg pants visually lengthen legs.",
                    "why_it_works": "High-waisted wide-leg pants visually lengthen legs while keeping you cool and elevated."
                },
                {
                    "id": "look_w_res_3",
                    "name": "LOOK 03 · Resort Co-Ord Elegance",
                    "description": "Botanical wrap top with matching flowy tiered maxi skirt.",
                    "items": {
                        "top": "Botanical print linen wrap crop top",
                        "bottom_or_dress": "Matching high-rise tiered maxi skirt",
                        "shoes": "Flat metallic leather gladiator sandals",
                        "outerwear": "None",
                        "accessories": "Natural cowrie shell choker & stacked bangles",
                        "bag": "Canvas travel tote",
                        "styling": "Messy boho braid with wet-look dew skin finish."
                    },
                    "colors": "Ocean Turquoise · Ivory · Coral",
                    "styling_tip": "Tiered maxi skirt moves gracefully with every step.",
                    "why_it_works": "Tiered maxi skirt moves gracefully with every step while defining waistline."
                }
            ]

    # Attach shopping search links to every item
    for look in looks:
        shopping = {}
        for key, val in look.get("items", {}).items():
            if val and str(val).lower() not in ["none", "n/a"]:
                shopping[key] = shopping_links(val, style, audience=audience, kids_age=kids_age)
        look["shopping"] = shopping

    return {
        "status": "success",
        "mode": "smart_engine",
        "looks": looks
    }


def fallback_chat_modify(message, profile, current_outfit):
    msg_lower = message.lower()
    reply_text = ""
    updated_outfit = None

    if current_outfit:
        updated_outfit = copy.deepcopy(current_outfit)
        items = updated_outfit.get("items", {})

        # 1. Footwear modification ("remove heels", "sandals", "sneakers")
        if "heel" in msg_lower or "shoe" in msg_lower or "sandal" in msg_lower or "flat" in msg_lower or "sneaker" in msg_lower:
            if "sandal" in msg_lower or "flat" in msg_lower or "no heel" in msg_lower or "remove heel" in msg_lower:
                items["shoes"] = "Minimalist flat metallic leather strappy sandals"
                reply_text = "I've replaced your heels with minimalist flat leather sandals so your outfit stays chic and comfortable!"
            elif "sneaker" in msg_lower or "casual" in msg_lower:
                items["shoes"] = "Retro multi-panel white leather sneakers"
                reply_text = "Swapped footwear to crisp white leather sneakers for a cool, casual street energy."
            else:
                items["shoes"] = "Pointed-toe leather pumps"
                reply_text = "Updated footwear to sleek pointed pumps."

        # 2. Bottom modification ("baggy", "bootcut", "jeans", "trousers", "skirt")
        elif "jean" in msg_lower or "pant" in msg_lower or "bottom" in msg_lower or "trouser" in msg_lower or "baggy" in msg_lower or "bootcut" in msg_lower:
            if "baggy" in msg_lower or "wide" in msg_lower or "relaxed" in msg_lower:
                items["bottom_or_dress"] = "High-waisted relaxed baggy blue denim jeans"
                reply_text = "Substituted the bottom with high-waisted relaxed baggy denim while preserving your top and footwear!"
            elif "bootcut" in msg_lower or "flare" in msg_lower:
                items["bottom_or_dress"] = "Dark-wash high-rise bootcut jeans"
                reply_text = "Swapped to dark-wash bootcut jeans to elongate your leg line while maintaining the rest of your outfit."
            else:
                items["bottom_or_dress"] = "Tailored wide-leg pleated beige trousers"
                reply_text = "Updated your bottom piece to tailored wide-leg trousers for a fresh aesthetic!"

        # 3. Outerwear / Jacket modification ("remove jacket", "no jacket", "cardigan")
        elif "jacket" in msg_lower or "coat" in msg_lower or "blazer" in msg_lower or "outerwear" in msg_lower:
            if "remove" in msg_lower or "no " in msg_lower or "don't want" in msg_lower or "without" in msg_lower:
                items["outerwear"] = "None"
                if "top" not in items or items.get("top", "").lower() in ["none", "n/a"]:
                    items["top"] = "Cute ribbed square-neck cotton top in cream"
                reply_text = "Removed the outerwear layer as requested and ensured your top and bottom are beautifully balanced."
            else:
                items["outerwear"] = "Oversized menswear blazer in camel beige"
                reply_text = "Updated outerwear layer to a camel beige oversized blazer."

        # 4. Aesthetic tweaks ("gen z", "trendy", "expensive", "luxury")
        elif "trendy" in msg_lower or "gen z" in msg_lower:
            items["accessories"] = "Tinted 90s oval sunglasses & layered silver link chains"
            reply_text = "Added retro 90s tinted shades and silver hardware for a trend-forward Gen Z edge!"

        elif "expensive" in msg_lower or "luxury" in msg_lower:
            items["bag"] = "Structured calfskin leather top-handle handbag"
            items["accessories"] = "Brushed 18k gold hoop earrings & fine wrist cuff"
            reply_text = "Upgraded handbag and accessories to calfskin leather and brushed gold for an opulent luxury finish."

        else:
            reply_text = f"Got it! I've tailored your outfit according to '{message}'."

        # Update shopping search links
        shopping = {}
        for k, v in items.items():
            if v and str(v).lower() not in ["none", "n/a"]:
                shopping[k] = shopping_links(v, profile.get("style", ""))
        updated_outfit["shopping"] = shopping

    else:
        # Direct chat generation fallback
        fallback_res = fallback_outfits(profile)
        updated_outfit = fallback_res["looks"][0]
        reply_text = f"✨ I've curated a complete look based on '{message}': {updated_outfit['name']}"

    return {
        "status": "success",
        "reply": reply_text,
        "updated_outfit": updated_outfit
    }


# =========================================================
# ROUTE: HOME / HEALTH CHECK
# =========================================================

@app.route("/")
def home():
    return jsonify({
        "status": "StyleMate AI backend is running",
        "ai_provider": "OpenAI (Active)" if client else "StyleMate Smart Engine (Fallback Active)"
    })


# =========================================================
# ROUTE: AI OUTFIT GENERATOR
# =========================================================

@app.route("/api/generate-outfit", methods=["POST"])
def generate_outfit():
    data = request.get_json(silent=True) or {}

    if not client:
        return jsonify(fallback_outfits(data))

    audience = data.get("audience", data.get("gender", "Women"))
    kids_age = data.get("kidsAge", "")
    body_type = data.get("bodyType", "")
    skin_tone = data.get("skinTone", "")
    colors = data.get("colors", [])
    if isinstance(colors, list):
        colors = ", ".join(colors)
    occasion = data.get("occasion", "")
    style = data.get("style", "")
    has_photo = bool(data.get("photo", ""))

    prompt = f"""
You are StyleMate, an elite personal AI fashion stylist (Zara/Vogue/COS level curation).
Generate 3 distinct, complete, highly wearable outfit recommendations for this user profile:

- Target Audience: {audience} {f'({kids_age})' if kids_age else ''}
- Body Type: {body_type}
- Skin Tone: {skin_tone}
- Preferred Colours: {colors}
- Occasion: {occasion}
- Vibe / Aesthetic: {style}
- User Uploaded Photo: {'Yes (Analyzed)' if has_photo else 'No'}

STRICT HARD CONSTRAINTS (PRIORITY ORDER):
1. USER TYPE / AGE (STRICT HARD CONSTRAINT):
   - If Target Audience is KIDS: NEVER recommend adult blazers, stilettos, corporate suits, evening gowns, or mature formalwear!
   - Outfits MUST be strictly age-appropriate, comfortable, tag-free, and playground-durable for {kids_age if kids_age else 'Kids'}.
   - Respect selected Kids Occasion ({occasion}) and Kids Aesthetic ({style}).

2. OCCASION (STRICT HARD CONSTRAINT):
   - Respect {occasion} strictly.

3. AESTHETIC: Reflect {style}.

4. BODY TYPE & SKIN TONE: Select flattering silhouettes, fits, necklines and color tones.

5. EVERY LOOK MUST BE A COMPLETE OUTFIT.
   Provide 3 distinct looks matching EXACTLY this JSON schema:

{{
  "status": "success",
  "looks": [
    {{
      "id": "look_1",
      "name": "LOOK 01 · Look Title",
      "description": "Short editorial description",
      "items": {{
        "top": "Specific top piece (or 'None' if dress/saree/lehenga)",
        "bottom_or_dress": "Specific bottom OR dress / saree / lehenga",
        "shoes": "Specific footwear (REQUIRED in every look)",
        "outerwear": "Specific jacket/blazer/layer or 'None'",
        "accessories": "Specific jewellery, watch or sunglasses",
        "bag": "Specific handbag, clutch, tote or backpack",
        "styling": "Specific hair, grooming and makeup advice"
      }},
      "colors": "Palette description (e.g. Ivory · Champagne · Beige)",
      "styling_tip": "Short key fit/styling tip",
      "why_it_works": "Why this specific complete outfit complements user type, age, occasion, body shape and skin tone"
    }},
    ... (total 3 looks)
  ]
}}

Return raw valid JSON only. Do not include markdown code fences.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are StyleMate AI. Always respond in strict valid raw JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        text_result = response.choices[0].message.content.strip()
        parsed = json.loads(text_result)

        # Attach shopping links
        for look in parsed.get("looks", []):
            shopping = {}
            for key, val in look.get("items", {}).items():
                if val and str(val).lower() not in ["none", "n/a"]:
                    shopping[key] = shopping_links(val, style, audience=audience, kids_age=kids_age)
            look["shopping"] = shopping

        return jsonify(parsed)

    except Exception as e:
        print("OPENAI API ERROR, Falling back to Smart Engine:", e)
        return jsonify(fallback_outfits(data))


# =========================================================
# ROUTE: AI CHATBOT (WITH OUTFIT MODIFICATION CONTEXT)
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()
    profile = data.get("profile", {})
    current_outfit = data.get("current_outfit", {})

    if not message:
        return jsonify({"reply": "Tell me what you'd like to adjust about your look!"})

    if not client:
        return jsonify(fallback_chat_modify(message, profile, current_outfit))

    # Call OpenAI Chat Completions with outfit context
    prompt = f"""
You are StyleMate, a friendly luxury AI personal fashion stylist.
The user is conversing with you about their outfit.

USER PROFILE:
{json.dumps(profile, indent=2)}

CURRENT ACTIVE OUTFIT JSON:
{json.dumps(current_outfit, indent=2)}

USER MESSAGE:
"{message}"

STRICT INSTRUCTIONS:
1. Identify WHICH PART of the outfit the user wants changed.
   - If user says "I don't want the jacket. Give me a cute top with these jeans", KEEP bottom (jeans), REMOVE jacket, ADD/CHANGE top. Do NOT modify the bottom piece.
   - If user says "Remove heels", replace footwear only.
   - If user says "Change jeans to baggy", replace bottom piece only.
   - If user asks for general style change ("Make it Gen Z", "Make it look expensive"), modify accessories/footwear while respecting age and occasion constraints.
2. Return a friendly conversational reply AND an updated outfit JSON object.
3. Return raw JSON matching this schema:

{{
  "reply": "Conversational friendly explanation of what you modified",
  "updated_outfit": {{ ... complete updated outfit object matching current_outfit structure ... }}
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are StyleMate AI. Always respond in strict valid raw JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        parsed = json.loads(response.choices[0].message.content.strip())
        if parsed.get("updated_outfit"):
            shopping = {}
            aud = profile.get("audience", "")
            age = profile.get("kidsAge", "")
            for k, v in parsed["updated_outfit"].get("items", {}).items():
                if v and str(v).lower() not in ["none", "n/a"]:
                    shopping[k] = shopping_links(v, profile.get("style", ""), audience=aud, kids_age=age)
            parsed["updated_outfit"]["shopping"] = shopping

        return jsonify(parsed)

    except Exception as e:
        print("CHAT API ERROR, Falling back to Smart Engine:", e)
        return jsonify(fallback_chat_modify(message, profile, current_outfit))


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )