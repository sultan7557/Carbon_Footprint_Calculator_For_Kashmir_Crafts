import os
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
from typing import Dict, Optional, List, Tuple
from app.models.schemas import PashminaInput
from app.config import MODEL_PATH, ENCODERS_PATH

class CarbonFootprintCalculator:
    def __init__(self):
        # Main Categories & Subcategories
        self.main_categories = [
            "Boutique",
            "Interior Decor",
            "Dining and Serving Ware",
            "Rugs and Carpets",
            "Furniture",
            "Ceiling Treatment",
            "Window Treatment",
            "Recycled Craft",
            "Sports Craft",
            "Hide Craft",
            "Culinary Craft",
            "Embroidery"
        ]
        self.subcategories = {
            "Boutique": [
                "Pashmina", "Kani Craft", "Cashmere", "Silk",
                "Kashmiri Bags and Purses", "Kashmiri Jackets",
                "Kaftans", "Kurtas", "Pherans", "Kashmiri Jewelry", "Sarongs"
            ],
            "Interior Decor": [
                "Papier-Mâché Items", "Bed Linens", "Room Divider Screens",
                "Office Accessories", "Jeweled Wall Hangings", "Tapestry",
                "Sofa and Cushion Covers"
            ],
            "Dining and Serving Ware": [
                "Copperware", "Silverware", "Walnutware", "Papier-Mâché Ware"
            ],
            "Rugs and Carpets": [
                "Rugs and Carpets", "Namda Embroidery Rugs"
            ],
            "Furniture": [
                "Walnut Wood Carving Furniture", "Crewel Furniture",
                "Wicker Furniture", "Room Dividers"
            ],
            "Ceiling Treatment": ["Khatamband"],
            "Window Treatment": [
                "Crewel Embroidery Curtains", "Pinjrakari - Kashmir Lattice Work"
            ],
            "Recycled Craft": ["Papier-Mâché", "Gabba"],
            "Sports Craft": ["Cricket-Bat", "Chess-Board"],
            "Hide Craft": ["Leather", "Fur & Astrakhan"],
            "Culinary Craft": ["Kashmiri Wazwan Canned Food", "Kahwa & Pink Tea"],
            "Embroidery": [
                "Suzani/Sozni - Fine NeedleWork", "Zardozi - Metal Thread Work",
                "Zalakdozi - Crewel Work", "Ari/Aari - Hook Work",
                "Dorukh - Double-sided Work", "Kashidakari - Surface Embroidery",
                "Jaaldar - Net Work", "Papier-Machie Inspired Embroidery"
            ]
        }

        # Emission Factors
        self.material_emissions = {
            # Existing Materials
            "Ultra-Fine Pashmina (10-12 microns)": 2.5,
            "Fine Pashmina (12-14 microns)": 2.5,
            "Standard Pashmina (14-16 microns)": 2.5,
            "Ultra-Fine Cashmere (13-15 microns)": 2.8,
            "Fine Cashmere (15-17 microns)": 2.8,
            "Standard Cashmere (17-19 microns)": 2.8,
            "Silver": 7.0, "Gold": 10.0, "Copper": 5.5, "Brass": 4.5, "Bronze": 6.5,
            "Silver Alloy": 5.0, "Plated Silver": 4.0, "Papier-Mâché": 2.5, "Wood": 5.5,
            "Cotton": 2.5, "Silk": 5.0, "Rattan": 1.2, "Reed": 1.1, "Bamboo": 1.5,
            "Wool": 3.5, "Blended Fabrics": 4.0, "Organic Cotton": 2.0, "Velvet": 2.0,
            "Organic Linen": 1.5, "Mulberry Silk": 5.0, "Tussar Silk": 4.0, "Eri Silk": 4.0,
            "Muga Silk": 4.0, "Raw Silk": 4.5, "Organza Silk": 5.0, "Kashmir Silk": 5.0,
            "Cotton Silk": 3.5, "Willow Wood": 4.0, "Willow Wicker": 2.5, "Synthetic Blend": 5.5,
            "Walnut with MDF Base": 5.0, "Synthetic/Composite Wood": 7.0, "Astrakhan Fur": 7.0,
            "Fur-Synthetic Blend": 5.0, "Synthetic Fur": 4.0,
            "Pashmina": 2.5, "Cashmere": 2.8, "Linen": 1.5, "Leather": 6.0, "Canvas": 2.0,
            "Jute": 1.8, "Chiffon": 2.2, "Khadi": 2.0, "Tweed": 3.0, "Blazer Fabric": 3.5,
            "Funnel Fabric": 3.2, "Semi-precious Stones": 4.0, "Pearls": 3.0, "Enamel": 2.5,
            # New Materials for Interior Decor
            "Waste Paper and Cotton Rags": 1.8,  # Papier-Mâché
            "Plant Fibers (such as Hemp)": 1.5,  # Papier-Mâché
            "Rice Flour Paste or Starch Paste": 1.0,  # Papier-Mâché
            "Fabric (Silk, Cotton)": 3.5,  # Jeweled Wall Hangings
            "Metal": 5.5, 
            "Walnut Wood": 5.0,
            "Wool-Cotton Blend": 4.0,
            "Kashmiri Walnut Wood - Grade A": 6.5,
            "Kashmiri Walnut Wood - Grade B": 6.0,
            "Kashmiri Walnut Wood - Grade C": 5.5,
            "Crewel-embroidered fabric": 4.0,
            "Rattan": 3.5,
            "Reed": 3.0,
            "Bamboo": 2.5,
            "Wicker": 3.0,
            "Fabric": 3.5,
            "Deodar Cedar": 5.0,
            "Fir Wood": 4.5,
            "Pine Wood": 4.0,
            "Local Softwoods": 3.5,
            "Kashmiri Walnut Wood": 6.0,
            "Silver Fir Wood": 4.5,
            "Blue Pine Wood": 4.0,
            "Organic Cotton": 1.8,
            "Kashmir Silk": 5.0,
            "Velvet": 3.8,
            "Organic Linen": 1.5,
            "Recycled Wool": 2.0,
            "Recycled Cotton": 1.5,
            "Recycled Silk": 3.0,
            "Recycled Fabric Threads": 1.8,
            "Kashmir Willow": 3.5,
            "Wood": 5.5,
            "Full-grain Leather": 6.5,  # Higher quality leather has slightly higher emissions
            "Top-grain Leather": 6.2,
            "Suede": 5.8,
            "Natural Fur (e.g., Mink, Fox)": 8.0,  # Higher emissions for natural fur
            "Faux Fur": 5.0,
            "Astrakhan (Karakul Lamb Fur)": 7.0,
            "Lamb": 6.5,
            "Mutton": 6.0,
            "Chicken": 3.5,
            "Beef": 8.0,
            "Goat": 5.5,
            "Fish": 3.0,
            "Vegetarian": 1.5,
            "Local Ingredients": 1.0,
            "Green Tea": 1.0,
            "Spices": 1.2,
            "Saffron": 2.5,  # Higher due to labor-intensive harvesting
            "Nuts": 1.8,
            "Fine Wool Threads (from Pashmina goats)": 2.5,
            "Pure Cotton Threads": 1.8,
            "Gold-plated silver threads (Kalabattu)": 5.0,
            "Silver-coated copper threads (modern alternative)": 4.0,
            "Silk Threads": 4.5,
            "Cotton Threads": 1.8,
            "Silk Threads (occasionally)": 4.0,
            "Fine Cotton Threads": 1.5,
            "Fine Wool Threads (pashmina quality)": 2.3,
            "Pashmina Threads": 2.5,

        }

        self.embedded_material_emissions = {
            "Wood": 5.5,
            "Fabric": 3.5,
            "Metal": 5.5
        }

        self.production_emissions = {
            # Existing Processes
            "Hand Spinning, Hand Weaving": 0.75, "Hand Spinning, Machine Weaving": 1.75,
            "Machine Spinning, Machine Weaving": 5.0, "Handcrafted": 2.5, "Machine-Made": 6.0,"Machine-made": 6.0,
            "Traditional Techniques": 2.0, "Hand-Knotted": 4.5, "Hand-Tufted": 3.5,
            "Hand-Weaving": 1.5, "Natural Material Treatment": 0.75,
            "Assembly Techniques": 4.0, "Handcrafted Techniques": 2.5, "Joinery Methods": 1.25,
            "Hand-Carved": 3.5, "Traditional Joinery": 3.0, "Hand Engraving (Simple)": 3.0,
            "Hand Engraving (Intricate)": 5.0, "Machine-Assisted Engraving": 4.0,
            "Hand Felting (Simple)": 2.5, "Machine-Assisted Felting": 4.5,
            "Hand Molding (Simple)": 1.5, "Machine-Assisted Molding": 3.5,
            "Hand Stitching (Simple)": 1.5, "Machine-Assisted Stitching": 3.5,
            "Hand Shaping (Simple)": 1.5, "Machine-Assisted Shaping": 3.5,
            "Sozni Embroidery (Simple)": 2.5, "Aari Work (Simple)": 1.5,
            "Chainstitch Embroidery (Simple)": 2.0, "Crewel Embroidery (Simple)": 2.0,
            "Machine Weaving": 3.0, "Machine Stitching": 3.5,
            # New Processes for Interior Decor
            "Traditional Paper Mâché Method": 2.0,  # Papier-Mâché
            "Molded Paper Mâché Process": 2.5,  # Papier-Mâché
            "Paper Mâché with Lacquer Finish": 3.0,
            "Natural material treatment": 1.3,
            "Handcrafted joinery": 2.0,  
            "Assembly techniques": 3.0,
            "Hand embroidery techniques": 2.5,
            "Chain Stitch": 1.2,
            "Satin Stitch": 1.3,
            "Blanket Stitch": 1.1,
            "Stem Stitch": 1.0,
            "Chain Stitch (Split Variation)": 1.2,
            "Herringbone Stitch": 1.4,
            "Couching Stitch": 1.3,
            "Flat Stitch": 0.9,
            "Raised Chain Stitch": 1.5,
            "French Knots": 1.6,
            "Traditional Techniques with Recycled Fabric": 1.5,
            "Machine-Assisted Weaving with Eco-Friendly Threads": 2.0,"Traditional Cooking": 2.5,
            "Modern Cooking": 1.5,
            "Cooking Process": 2.5,
            "Traditional Brewing": 1.5,
            "Modern Brewing": 1.0,
            "Single-thread technique": 1.2,
            "Very fine stitches": 1.4,
            "Dense parallel lines": 1.5,
            "Layered color work": 1.7,
            "Surface satin construction": 1.6,
            "Even stitch spacing": 1.3,
            "Metal thread couching": 2.0,
            "Underlay preparation": 1.5,
            "Framework stitching": 1.7,
            "Raised work technique": 2.2,
            "Metal component anchoring": 2.0,
            "Padding technique": 1.8,
            "Long-short technique": 1.4,
            "Pattern filling": 1.5,
            "Directional stitching": 1.3,
            "Texture building": 1.6,
            "Relief work creation": 1.8,
            "Surface coverage": 1.5,
            "Hook work technique": 1.7,
            "Frame-mounted construction": 1.9,
            "Chain stitch formation": 1.4,
            "Bead attachment": 1.6,
            "Sequin work": 1.8,
            "Surface embellishment": 1.7,
            "Double-sided construction": 2.0,
            "No-knot technique": 1.5,
            "Clean reverse method": 1.6,
            "Identical stitch formation": 1.7,
            "Mirror-image working": 1.8,
            "Hidden thread endings": 1.4,
            "Chain stitch construction": 1.3,
            "Pattern building": 1.4,
            "Color blending": 1.5,
            "Design framework": 1.6,
            "Motif development": 1.7,
            "Thread pulling technique": 1.5,
            "Grid formation": 1.6,
            "Systematic hole creation": 1.7,
            "Even tension network": 1.8,
            "Geometric framework building": 1.9,
            "Regular interval spacing": 1.4,
            "Layer building technique": 1.6,
            "Color gradation work": 1.7,
            "Motif outlining": 1.5,
            "Shading technique": 1.8,
            "Dimensional effect creation": 1.9
        }

        self.dye_emissions = {
            "Natural-Dyed": 0.75, "Vegetable-Dyed": 0.75, "Chemical-Dyed": 2.0, "Eco-Dyed": 0.75,
            "Acid-Dyed": 1.8, "Azo-Free Dyed": 1.0, "Tie-Dyed": 1.5, "Ombre-Dyed": 1.7,
            "Hand-Painted or Brush-Dyed": 1.75, "Hand-Painted": 1.75, "Lacquer Finish": 2.0,
            "Natural Varnish": 1.0, "Decorative Painting": 2.5, "Glossy Finish": 1.5,
            "Matte Finish": 1.2, "Polished Finish": 1.5, "Antiqued Finish": 1.5,
            "Hammered Finish": 1.8, "Stained Finish": 1.2, "Textured Finishes": 1.5,
            "Varnished": 1.0, "Lacquered": 1.75, "Natural Sealing": 1.0,
            "Protective Coatings": 1.2, "Natural Finish": 0.75, "Waxed": 1.3,
            "Natural Leather Finish": 0.75, "Hand-polished": 0.75, "Standard Finish": 1.0,
            "Chain Stitch": 1.2, "Oxidized Finish": 1.6, "Enamel Work": 2.0,
            # New Finishing Techniques for Interior Decor
            "Gold/Silver Leaf Application": 2.2,  # Papier-Mâché
            "Fringing": 1.0,  # Tapestry, Jeweled Wall Hangings
            "Backing": 1.2,  # Tapestry, Jeweled Wall Hangings
            "Binding": 1.1,  # Tapestry, Jeweled Wall Hangings
            "Lining": 1.3,  # Tapestry, Jeweled Wall Hangings
            "Mounting": 1.4,  # Tapestry, Jeweled Wall Hangings
            "Stiffening": 1.5,  # Tapestry, Jeweled Wall Hangings
            "Embroidered": 2.0,  # Sofa and Cushion Covers, Bed Linens
            "Screen-Printed": 1.8,  # Sofa and Cushion Covers, Bed Linens
            "Block-Printed": 1.9,  
            "Natural Finish": 0.75,
            "Lacquered Finish": 1.2, 
            "Stained Finish": 1.0,
            "Fringed Edges": 1.0,
            "Bound Edges": 1.2,
            "Double-Sided Finish": 1.5,
            "Matte Finish": 1.2,
            "Glossy Finish": 1.5,
            "Semi-Gloss Finish": 1.3,
            "Hand-stitched edges": 0.8,
            "Lining and backing finishes": 1.0,
            "Natural Sealing": 0.7,
            "Protective Coatings": 1.2,
            "Staining": 1.1,
            "Painting": 1.4,
            "Handwoven Edges": 0.8,
            "Woolen Pile Finish": 1.2,
            "Distressed or Antique Finish": 1.0,
            "Hand-polished": 0.75,
            "Custom Varnish Finish": 1.0,
            "Sanding": 0.5,
            "Hand-polished for smooth surface and longevity": 0.75,
            "Wood-stained or lacquered for protection": 1.0,
            "Waxed for a smooth and shiny surface": 1.2,
            "Stained or dyed to enhance color depth and richness": 1.4,
            "Natural Leather Finish for a rustic look": 0.9,
            "Fur Brushed for smoothness and volume": 0.8,
            "Curled or Crimped for added texture": 1.1,
            "Dyed for vibrant and customized colors": 1.5,


        }

        self.packaging_emissions = {
            "Fabric Wrapping": 0.5, "Luxury Gift Boxes": 2.5, "Protective Sleeves": 1.0,
            "Hang Tags": 0.2, "Basic": 0.75, "Luxury Papier Mache": 2.5, "Plastic": 1.5,
            "Custom-fit Boxes": 1.5, "Eco-friendly Packaging Materials": 1.25,
            "Wooden Crates": 2.5, "Protective Wrap": 1.0, "Curtain Bags": 0.7,
            "Leather Boxes": 1.8, "Custom-fit Crates/Boxes": 1.8,
            "Canned": 1.8,
            "Glass Jars": 1.5,
            "Flexible Pouches": 0.8,
            "Tin Boxes": 1.7,
            "Paper Boxes": 0.9,
            "Vacuum-Sealed Pouches": 1.0,
            "Glass Bottles": 1.6,  
            "Tea Bags": 0.7,       # Lightweight paper packaging
            "Pouches": 0.8,        
            "Paper Machie Boxes": 1.0 
        }

        self.transportation_emissions = {
            "Sea": 2.5, "Air": 6.5, "Local": 0.75, "Domestic": 2.0
        }

        self.certification_emissions = {
            # Existing Certifications
            "GI Certificate": 0.1, "Responsible Wool Standard (RWS)": 0.15,
            "Blockchain Traceability": 0.2, "Handloom Mark": 0.1,
            "Woolmark Certification": 0.15, "Global Organic Textile Standard (GOTS)": 0.2,
            "OEKO-TEX Standard 100": 0.15, "OEKO-TEX® Standard 100": 0.15, "Fair Trade Certification": 0.2,
            "Customs and Import Certifications": 0.1, "Cradle to Cradle Certification": 0.25,
            "Cashmere Certification Program (CCP)": 0.15, "Sustainable Cashmere Certification": 0.2,
            "The Good Cashmere Standard®": 0.2, "Silk Mark Certification": 0.15,
            "ISO 14001 (Environmental Management)": 0.2, "Sustainable Apparel Coalition’s Higg Index": 0.25, "None": 0.0,
            "Organic Content Standard (OCS)": 0.15, "Leather Working Group (LWG) Certification": 0.2,
            "PETA-Approved Vegan Certification": 0.15, "ISO 9001": 0.15, "GI Certification": 0.1, "ISO 9001 (Quality Management)": 0.15,
            "Hallmarking, RJC Certification, Fairmined, Conflict-Free (e.g., Kimberley Process)": 0.2,
            "Gemological Institute of America (GIA) Certification": 0.15,
            "International Gemological Institute (IGI) Certification": 0.15,
            "Colored Gemstone Certification": 0.15, "American Gem Society (AGS) Certification": 0.15,
            "Jewelry Council of America (JCA) Certification": 0.15, "Ethical Gemstone Certification": 0.2,
            # Certifications for Interior Decor
            "Geographical Indication (GI) Certification": 0.1,  # Papier-Mâché
            "Hallmarking for Jewelry": 0.15,  # Jeweled Wall Hangings
            "Responsible Jewelry Council (RJC) Certification": 0.2,  # Jeweled Wall Hangings
            "Forest Stewardship Council (FSC) Certification": 0.15, 
            "Fairmined Gold Certification (if applicable)": 0.2,
            "Handcrafted Quality Certification": 0.1,
            "Eco-Friendly Certification": 0.2,
            "FSC Certification (if using wood or natural materials)": 0.15,
            "Geographical Indication (GI) Certification": 0.1,
            "FSC Certification (Forest Stewardship Council)": 0.15,
            "Product Safety Certifications": 0.1,
            "Leather Working Group (LWG) Certification": 0.2,
            "CITES Certification (for products involving endangered species)": 0.1,
            "FSSAI Certification": 0.1,
            "ISO 22000 (Food Safety Management System)": 0.2,
            "Organic Certification": 0.15,
            "Halal Certification": 0.1,
        }

        self.weaving_emissions = {
            "Twill Weave": 0.5, "Diamond Weave": 0.7, "Herringbone Weave": 0.6,
            "Jacquard Weave": 1.0, "Plain Weave": 0.4, "Honeycomb Weave": 0.8,
            "Satin Weave": 0.6, "Organza Weave": 0.5, "Brocade Weave": 1.2,
            "Crepe Weave": 0.7, "Chiffon Weave": 0.5, "Georgette Weave": 0.6
        }

        self.shipping_categories = {
            "local": {"max_distance": 1000, "factor": 0.0002},
            "regional": {"max_distance": 5000, "factor": 0.00025},
            "international": {"max_distance": 10000, "factor": 0.0003},
            "global": {"max_distance": 20000, "factor": 0.00035}
        }

        self.shipping_volume_factors = {
            "Individual": 1.0,
            "Bulk": 0.8
        }

        self.default_processing = {
            "Boutique": "Hand Spinning, Hand Weaving",
            "Interior Decor": "Handcrafted Techniques",
            "Dining and Serving Ware": "Handcrafted",
            "Rugs and Carpets": "Hand-Knotted",
            "Furniture": "Hand-Carved",
            "Ceiling Treatment": "Handcrafted Techniques",
            "Window Treatment": "Traditional Joinery",
            "Recycled Craft": "Hand Molding (Simple)",
            "Sports Craft": "Hand Shaping (Simple)",
            "Hide Craft": "Hand Stitching (Simple)",
            "Culinary Craft": "Handcrafted",
            "Embroidery": "Sozni Embroidery (Simple)"
        }

        self.default_crafting = {
            "Boutique": "Natural-Dyed",
            "Interior Decor": "Hand-Painted",
            "Dining and Serving Ware": "Hand-polished",
            "Rugs and Carpets": "",
            "Furniture": "Matte Finish",
            "Ceiling Treatment": "Lacquer Finish",
            "Window Treatment": "Natural Finish",
            "Recycled Craft": "Varnished",
            "Sports Craft": "Natural Sealing",
            "Hide Craft": "Natural Leather Finish",
            "Culinary Craft": "Hand-polished",
            "Embroidery": "Chain Stitch"
        }

        self.model = None
        self.label_encoders = {}
        self._load_or_train_model()

    def _load_or_train_model(self):
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
                self.model = joblib.load(MODEL_PATH)
                self.label_encoders = joblib.load(ENCODERS_PATH)
            else:
                self.train_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self.train_model()

    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        data = {
            "craft_category": [],
            "craft_type": [],
            "raw_material": [],
            "embedded_material": [],
            "processing": [],
            "crafting": [],
            "packaging": [],
            "transportation": [],
            "certifications": [],
            "weaving_design": [],
            "finishing_technique": [],
            "shipping_distance": np.random.uniform(0, 10000, n_samples)
        }

        for i in range(n_samples):
            chosen_category = np.random.choice(self.main_categories)
            data["craft_category"].append(chosen_category)
            subcat_options = self.subcategories.get(chosen_category, ["Default Subcategory"])
            craft_type = np.random.choice(subcat_options)
            data["craft_type"].append(craft_type)
            data["raw_material"].append(np.random.choice(list(self.material_emissions.keys())))
            if craft_type == "Papier-Mâché Items":
                data["embedded_material"].append(np.random.choice(list(self.embedded_material_emissions.keys())))
            else:
                data["embedded_material"].append(None)
            data["processing"].append(np.random.choice(list(self.production_emissions.keys())))
            data["crafting"].append(np.random.choice(list(self.dye_emissions.keys())))
            data["packaging"].append(np.random.choice(list(self.packaging_emissions.keys())))
            data["transportation"].append(np.random.choice(list(self.transportation_emissions.keys())))
            data["certifications"].append(np.random.choice(list(self.certification_emissions.keys())))
            if craft_type in ["Cashmere", "Silk", "Kashmiri Bags and Purses", "Kashmiri Jackets", "Kaftans", "Kurtas", "Pherans", "Kashmiri Jewelry"]:
                data["weaving_design"].append(np.random.choice(list(self.weaving_emissions.keys())))
            else:
                data["weaving_design"].append(None)
            if craft_type in ["Papier-Mâché Items", "Tapestry", "Jeweled Wall Hangings", "Office Accessories", "Room Divider Screens", "Sofa and Cushion Covers", "Bed Linens"]:
                finishing_options = list(self.dye_emissions.keys())
                data["finishing_technique"].append(np.random.choice(finishing_options))
            else:
                data["finishing_technique"].append(None)

        carbon_footprint = []
        for i in range(n_samples):
            base_emissions = (
                self.material_emissions[data["raw_material"][i]] +
                (self.embedded_material_emissions[data["embedded_material"][i]] if data["embedded_material"][i] else 0) +
                self.production_emissions[data["processing"][i]] +
                self.dye_emissions[data["crafting"][i]] +
                self.packaging_emissions[data["packaging"][i]] +
                self.transportation_emissions[data["transportation"][i]] +
                self.certification_emissions[data["certifications"][i]] +
                (self.weaving_emissions[data["weaving_design"][i]] if data["weaving_design"][i] else 0) +
                (self.dye_emissions[data["finishing_technique"][i]] if data["finishing_technique"][i] else 0) +
                self._get_shipping_factor(data["shipping_distance"][i]) * data["shipping_distance"][i]
            )
            noise = np.random.normal(0, 0.5)
            carbon_footprint.append(base_emissions + noise)

        data["carbon_footprint"] = carbon_footprint
        return pd.DataFrame(data)

    def train_model(self):
        training_data = self.generate_synthetic_data()
        feature_cols = [
            "raw_material", "embedded_material", "processing", "crafting", "packaging",
            "transportation", "certifications", "weaving_design", "finishing_technique",
            "shipping_distance"
        ]
        X = training_data[feature_cols]
        y = training_data["carbon_footprint"]

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

        for column in X.select_dtypes(include=["object"]):
            self.label_encoders[column] = LabelEncoder()
            X[column] = X[column].fillna("None")
            X[column] = self.label_encoders[column].fit_transform(X[column])

        self.model.fit(X, y)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(ENCODERS_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.label_encoders, ENCODERS_PATH)

    def _predict_missing_values(self, input_data: PashminaInput) -> Tuple[Dict, List[str]]:
        predictions = {}
        explanations = []
        dont_know = "I don’t know"

        if not input_data.craft_category or input_data.craft_category == dont_know:
            predictions["craft_category"] = "Boutique"

        craft_cat = input_data.craft_category if input_data.craft_category and input_data.craft_category != dont_know else predictions.get("craft_category", "Boutique")

        if not input_data.craft_type or input_data.craft_type == dont_know:
            subcat_options = self.subcategories.get(craft_cat, ["Pashmina"])
            predictions["craft_type"] = subcat_options[0]

        craft_type = input_data.craft_type if input_data.craft_type and input_data.craft_type != dont_know else predictions.get("craft_type")

        if not input_data.raw_material or input_data.raw_material == dont_know:
            if craft_cat == "Boutique":
                if craft_type == "Pashmina":
                    predictions["raw_material"] = "Standard Pashmina (14-16 microns)"
                elif craft_type == "Cashmere":
                    predictions["raw_material"] = "Standard Cashmere (17-19 microns)"
                elif craft_type == "Sarongs":
                    predictions["raw_material"] = "Cotton"
                elif craft_type == "Kashmiri Bags and Purses":
                    predictions["raw_material"] = "Wool"
                elif craft_type == "Kashmiri Jackets":
                    predictions["raw_material"] = "Pashmina"
                elif craft_type == "Kaftans":
                    predictions["raw_material"] = "Silk"
                elif craft_type == "Kurtas":
                    predictions["raw_material"] = "Cotton"
                elif craft_type == "Pherans":
                    predictions["raw_material"] = "Wool"
                elif craft_type == "Kashmiri Jewelry":
                    predictions["raw_material"] = "Silver"
            elif craft_cat == "Interior Decor":
                if craft_type == "Papier-Mâché Items":
                    predictions["raw_material"] = "Waste Paper and Cotton Rags"
                elif craft_type == "Tapestry":
                    predictions["raw_material"] = "Wool"
                elif craft_type == "Jeweled Wall Hangings":
                    predictions["raw_material"] = "Fabric (Silk, Cotton)"
                elif craft_type == "Office Accessories":
                    predictions["raw_material"] = "Wood"
                elif craft_type == "Room Divider Screens":
                    predictions["raw_material"] = "Wood"
                elif craft_type == "Sofa and Cushion Covers":
                    predictions["raw_material"] = "Cotton"
                elif craft_type == "Bed Linens":
                    predictions["raw_material"] = "Cotton"
            elif craft_cat == "Dining and Serving Ware":
                predictions["raw_material"] = "Copper"
            elif craft_cat == "Furniture":
                predictions["raw_material"] = "Wood"
            elif craft_type == "Namda Embroidery Rugs":
                predictions["finishing_technique"] = "Fringed Edges"
            elif craft_cat == "Furniture":
                if craft_type == "Walnut Wood Carving Furniture":
                    predictions["raw_material"] = "Kashmiri Walnut Wood - Grade B"
                    predictions["finishing_technique"] = "Matte Finish"
                elif craft_type == "Crewel Furniture":
                    predictions["raw_material"] = "Crewel-embroidered fabric"
                    predictions["finishing_technique"] = "Hand-stitched edges"
                elif craft_type == "Wicker Furniture":
                    predictions["raw_material"] = "Rattan"
                    predictions["finishing_technique"] = "Natural Sealing"
                elif craft_type == "Room Dividers":
                    predictions["raw_material"] = "Wood"
                    predictions["finishing_technique"] = "Natural Sealing"
                else:
                    predictions["raw_material"] = "Wood"
            elif craft_cat == "Ceiling Treatment":
                if craft_type == "Khatamband":
                    predictions["raw_material"] = "Kashmiri Walnut Wood"
                    predictions["finishing_technique"] = "Natural Finish"
            elif craft_cat == "Window Treatment":
                if craft_type == "Pinjrakari - Kashmir Lattice Work":
                    predictions["raw_material"] = "Walnut Wood"
                    predictions["finishing_technique"] = "Natural Finish"
                elif craft_type == "Crewel - Embroidery Curtains":
                    predictions["raw_material"] = "Organic Cotton"
            elif craft_cat == "Recycled Craft":
                if craft_type == "Papier-Mâché":
                    predictions["raw_material"] = "Waste Paper and Cotton Rags"
                    predictions["embedded_material"] = "Wood"
                    predictions["finishing_technique"] = "Hand-Painted"
                elif craft_type == "Gabba":
                    predictions["raw_material"] = "Recycled Wool"
                    predictions["finishing_technique"] = "Handwoven Edges"
            elif craft_cat == "Sports Craft":
                if craft_type == "Cricket-Bat":
                    predictions["raw_material"] = "Willow Wood"
                    predictions["finishing_technique"] = "Hand-polished"
                elif craft_type == "Chess-Board":
                    predictions["raw_material"] = "Wood"
                    predictions["finishing_technique"] = "Hand-polished for smooth surface and longevity"
            elif craft_cat == "Hide Craft":
                if craft_type == "Leather":
                    predictions["raw_material"] = "Full-grain Leather"
                    predictions["finishing_technique"] = "Natural Leather Finish for a rustic look"
                elif craft_type == "Fur & Astrakhan":
                    predictions["raw_material"] = "Faux Fur" 
                    predictions["finishing_technique"] = "Fur Brushed for smoothness and volume"
            elif craft_cat == "Culinary Craft":
                if craft_type == "Kashmiri Wazwan Canned Food":
                    predictions["raw_material"] = "Lamb"
                    predictions["processing"] = "Traditional Cooking"
                    predictions["packaging"] = "Canned"
                elif craft_type == "Kahwa & Pink Tea":
                    predictions["raw_material"] = "Local Ingredients"
                    predictions["processing"] = "Traditional Brewing"
                    predictions["packaging"] = "Paper Machie Boxes"
            elif craft_cat == "Embroidery":
                if craft_type == "Suzani/Sozni - Fine NeedleWork":
                    predictions["raw_material"] = "Fine Wool Threads (from Pashmina goats)"
                    predictions["fabric_choice"] = "Pure Pashmina"
                    predictions["processing"] = "Single-thread technique"
                elif craft_type == "Zardozi - Metal Thread Work":
                    predictions["raw_material"] = "Gold-plated silver threads (Kalabattu)"
                    predictions["fabric_choice"] = "Velvet"
                    predictions["processing"] = "Metal thread couching"
                elif craft_type == "Zalakdozi - Crewel Work":
                    predictions["raw_material"] = "Cotton Threads"
                    predictions["fabric_choice"] = "Cotton Duck"
                    predictions["processing"] = "Long-short technique"
                elif craft_type == "Ari/Aari - Hook Work":
                    predictions["raw_material"] = "Silk Threads"
                    predictions["fabric_choice"] = "Silk"
                    predictions["processing"] = "Hook work technique"
                elif craft_type == "Dorukh - Double-sided Work":
                    predictions["raw_material"] = "Fine Cotton Threads"
                    predictions["fabric_choice"] = "Fine Muslin"
                    predictions["processing"] = "Double-sided construction"
                elif craft_type == "Kashidakari - Surface Embroidery":
                    predictions["raw_material"] = "Cotton Threads"
                    predictions["fabric_choice"] = "Woolen Base"
                    predictions["processing"] = "Chain stitch construction"
                elif craft_type == "Jaaldar - Net Work":
                    predictions["raw_material"] = "Silk Threads"
                    predictions["fabric_choice"] = "Fine Cotton"
                    predictions["processing"] = "Thread pulling technique"
                elif craft_type == "Papier-Machie Inspired Embroidery":
                    predictions["raw_material"] = "Silk Threads"
                    predictions["fabric_choice"] = "Velvet"
                    predictions["processing"] = "Layer building technique"
            else:
                predictions["raw_material"] = "Cotton"

        if not input_data.embedded_material or input_data.embedded_material == dont_know:
            predictions["embedded_material"] = "Wood" if craft_type == "Papier-Mâché Items" else None

        if not input_data.processing or input_data.processing == dont_know:
            predictions["processing"] = self.default_processing.get(craft_cat, "Handcrafted")

        if not input_data.crafting or input_data.crafting == dont_know:
            predictions["crafting"] = self.default_crafting.get(craft_cat, "Natural-Dyed")

        if not input_data.packaging or input_data.packaging == dont_know:
            predictions["packaging"] = "Fabric Wrapping"

        if not input_data.transportation or input_data.transportation == dont_know:
            predictions["transportation"] = "Local"

        if not input_data.shipping_distance or input_data.shipping_distance == dont_know:
            predictions["shipping_distance"] = 1000

        if not input_data.shipping_volume or input_data.shipping_volume == dont_know:
            predictions["shipping_volume"] = "Individual"

        if not input_data.shipping_location or input_data.shipping_location == dont_know:
            predictions["shipping_location"] = "Kashmir"

        if not input_data.dkc_warehouse or input_data.dkc_warehouse == dont_know:
            predictions["dkc_warehouse"] = "West Coast"

        if not input_data.certifications or input_data.certifications == dont_know:
            predictions["certifications"] = "None"

        if not input_data.weaving_design or input_data.weaving_design == dont_know:
            predictions["weaving_design"] = "Plain Weave" if craft_type in ["Pashmina", "Cashmere", "Silk", "Kashmiri Bags and Purses", "Kashmiri Jackets", "Kaftans", "Kurtas", "Pherans", "Kashmiri Jewelry"] else None

        if not input_data.finishing_technique or input_data.finishing_technique == dont_know:
            if craft_type == "Papier-Mâché Items":
                predictions["finishing_technique"] = "Hand-Painted"
            elif craft_type == "Tapestry":
                predictions["finishing_technique"] = "Fringing"
            elif craft_type == "Jeweled Wall Hangings":
                predictions["finishing_technique"] = "Fringing"
            elif craft_type == "Office Accessories":
                predictions["finishing_technique"] = "Hand-Painted"
            elif craft_type == "Room Divider Screens":
                predictions["finishing_technique"] = "Hand-Painted"
            elif craft_type == "Sofa and Cushion Covers":
                predictions["finishing_technique"] = "Hand-Painted"
            elif craft_type == "Bed Linens":
                predictions["finishing_technique"] = "Hand-Painted"
            elif craft_type == "Kashmiri Jewelry":
                predictions["finishing_technique"] = "Polished Finish"
            elif craft_type == "Papier-Mâché Ware":
                predictions["finishing_technique"] = "Polished Finish"
            elif craft_type == "Walnutware":
                predictions["finishing_technique"] = "Natural Finish"
            elif craft_type == "Silverware":
                predictions["finishing_technique"] = "Polished Finish"
            elif craft_type == "Copperware":
                predictions["finishing_technique"] = "Polished Finish"
            else:
                predictions["finishing_technique"] = None

        return predictions, explanations

    def _generate_detailed_recommendations(self, input_data: PashminaInput, predictions: Dict, carbon_footprint: float) -> Tuple[List[str], List[str]]:
        recommendations = []
        explanations = []

        raw_material = input_data.raw_material if input_data.raw_material != "I don’t know" else predictions.get("raw_material")
        embedded_material = input_data.embedded_material if input_data.embedded_material != "I don’t know" else predictions.get("embedded_material")
        processing = input_data.processing if input_data.processing != "I don’t know" else predictions.get("processing")
        crafting = input_data.crafting if input_data.crafting != "I don’t know" else predictions.get("crafting")
        packaging = input_data.packaging if input_data.packaging != "I don’t know" else predictions.get("packaging")
        transportation = input_data.transportation if input_data.transportation != "I don’t know" else predictions.get("transportation")
        shipping_distance = input_data.shipping_distance if input_data.shipping_distance != "I don’t know" else predictions.get("shipping_distance")
        certifications = input_data.certifications if input_data.certifications != "I don’t know" else predictions.get("certifications")
        weaving_design = input_data.weaving_design if input_data.weaving_design != "I don’t know" else predictions.get("weaving_design")
        finishing_technique = input_data.finishing_technique if input_data.finishing_technique != "I don’t know" else predictions.get("finishing_technique")

        # Processing Recommendations
        if processing in ["Machine Spinning, Machine Weaving", "Machine Weaving", "Machine Stitching", "Machine-Made"]:
            recommendations.append("Consider switching to hand processes for lower emissions.")
            explanations.append("Machine-based processes contribute higher emissions.")
        elif processing in ["Hand Spinning, Hand Weaving", "Hand Weaving", "Handcrafted", "Traditional Techniques", "Traditional Paper Mâché Method"]:
            recommendations.append("Maintain hand processes for low emissions.")
            explanations.append("Hand processes are low-emission.")

        # Crafting Recommendations
        if crafting in ["Chemical-Dyed", "Acid-Dyed"]:
            recommendations.append("Switch to natural or eco-dyes to reduce emissions.")
            explanations.append("Chemical and acid dyes have a higher environmental impact.")
        elif crafting in ["Natural-Dyed", "Vegetable-Dyed", "Eco-Dyed"]:
            recommendations.append("Continue using sustainable dyeing methods.")
            explanations.append("Natural and eco-dyes are environmentally friendly.")

        # Packaging Recommendations
        if packaging in ["Custom-fit Boxes"]:
            recommendations.append("Switch to eco-friendly packaging for lower emissions.")
            explanations.append("Custom-fit boxes have moderate emissions.")
        elif packaging in ["Eco-friendly Packaging Materials"]:
            recommendations.append("Your packaging choice is sustainable; keep it up.")
            explanations.append("Eco-friendly materials have low emissions.")

        # Transportation Recommendations
        if transportation in ["Air"]:
            recommendations.append("Switch from air to sea transport to lower emissions.")
            explanations.append("Air transport has significantly higher emissions.")
        elif transportation in ["Local"]:
            recommendations.append("Local transport is optimal; maintain this approach.")
            explanations.append("Local transport minimizes emissions.")

        # Shipping Distance Recommendations
        if shipping_distance and float(shipping_distance) > 5000:
            recommendations.append("Reduce shipping distance with regional hubs.")
            explanations.append("Long shipping distances increase emissions.")
        elif shipping_distance and float(shipping_distance) < 1000:
            recommendations.append("Short distances are great; optimize logistics.")
            explanations.append("Short shipping distances keep emissions low.")

        # Raw Material Recommendations
        if raw_material in ["Leather", "Gold", "Metal"]:
            recommendations.append("Consider lower-impact alternatives (e.g., cotton, plant fibers) to reduce emissions.")
            explanations.append("High-impact materials like leather and metals increase emissions.")
        elif raw_material in ["Cotton", "Khadi", "Linen", "Waste Paper and Cotton Rags"]:
            recommendations.append("Sustainable raw material choice; maintain this approach.")
            explanations.append("Cotton, khadi, linen, and recycled materials have lower emissions.")

        # Embedded Material Recommendations (Papier-Mâché)
        if embedded_material == "Metal":
            recommendations.append("Consider using fabric or wood as embedded materials to reduce emissions.")
            explanations.append("Metal as an embedded material has a higher environmental impact.")
        elif embedded_material in ["Wood", "Fabric"]:
            recommendations.append("Sustainable embedded material choice; maintain this approach.")
            explanations.append("Wood and fabric have moderate to low emissions.")

        # Certification Recommendations
        if certifications == "None":
            recommendations.append("Consider obtaining a sustainability certification (e.g., GOTS) to improve eco-credentials.")
            explanations.append("Certifications can signal sustainable practices but add minor emissions.")
        elif certifications in ["Cradle to Cradle Certification*", "Sustainable Apparel Coalition’s Higg Index"]:
            recommendations.append("High-impact certification; ensure it aligns with overall sustainability goals.")
            explanations.append("These certifications involve more extensive processes, slightly increasing emissions.")

        # Weaving Design Recommendations
        if weaving_design in ["Jacquard Weave", "Brocade Weave"]:
            recommendations.append("Consider simpler weaves like Plain Weave to reduce emissions.")
            explanations.append("Complex weaves like Jacquard or Brocade require more energy.")
        elif weaving_design == "Plain Weave":
            recommendations.append("Plain Weave is a low-emission choice; maintain this approach.")
            explanations.append("Simpler weaves minimize energy use.")

        # Finishing Technique Recommendations
        if finishing_technique in ["Gold/Silver Leaf Application", "Embroidered"]:
            recommendations.append("Consider simpler finishes like Hand-Painted to reduce emissions.")
            explanations.append("Complex finishes like gold/silver leaf or embroidery involve additional materials and energy.")
        elif finishing_technique == "Hand-Painted":
            recommendations.append("Hand-Painted is a low-emission choice; maintain this approach.")
            explanations.append("Simple finishes minimize environmental impact.")

        # General Recommendation
        if carbon_footprint > 10:
            recommendations.append("High footprint; review all inputs for sustainability.")
            explanations.append("Total emissions exceed typical sustainable thresholds.")
        elif carbon_footprint < 5:
            recommendations.append("Low footprint; keep up the good work!")
            explanations.append("Total emissions are within sustainable limits.")

        return recommendations, explanations

    def predict_carbon_footprint(self, input_data: PashminaInput) -> dict:
        try:
            predictions, _ = self._predict_missing_values(input_data)

            # Create input DataFrame
            input_dict = {
                "craft_category": input_data.craft_category if input_data.craft_category != "I don't know" else predictions.get("craft_category"),
                "craft_type": input_data.craft_type if input_data.craft_type != "I don't know" else predictions.get("craft_type"),
                "raw_material": input_data.raw_material if input_data.raw_material != "I don't know" else predictions.get("raw_material"),
                "embedded_material": input_data.embedded_material if input_data.embedded_material != "I don't know" else predictions.get("embedded_material"),
                "processing": input_data.processing if input_data.processing != "I don't know" else predictions.get("processing"),
                "crafting": input_data.crafting if input_data.crafting != "I don't know" else predictions.get("crafting"),
                "packaging": input_data.packaging if input_data.packaging != "I don't know" else predictions.get("packaging"),
                "transportation": input_data.transportation if input_data.transportation != "I don't know" else predictions.get("transportation"),
                "shipping_volume": input_data.shipping_volume if input_data.shipping_volume != "I don't know" else predictions.get("shipping_volume"),
                "shipping_location": input_data.shipping_location if input_data.shipping_location != "I don't know" else predictions.get("shipping_location"),
                "dkc_warehouse": input_data.dkc_warehouse if input_data.dkc_warehouse != "I don't know" else predictions.get("dkc_warehouse"),
                "certifications": input_data.certifications if input_data.certifications != "I don't know" else predictions.get("certifications"),
                "weaving_design": input_data.weaving_design if input_data.weaving_design != "I don't know" else predictions.get("weaving_design"),
                "finishing_technique": input_data.finishing_technique if input_data.finishing_technique != "I don't know" else predictions.get("finishing_technique")
            }
            
            # Add fabric_choice if it exists
            if hasattr(input_data, "fabric_choice"):
                input_dict["fabric_choice"] = input_data.fabric_choice if input_data.fabric_choice != "I don't know" else predictions.get("fabric_choice")
            
            input_df = pd.DataFrame([input_dict])

            # Calculate shipping emission
            shipping_distance_val = input_data.shipping_distance
            if shipping_distance_val is not None and shipping_distance_val != "I don't know":
                try:
                    shipping_distance = float(shipping_distance_val)
                except ValueError:
                    shipping_distance = 1000  # Default if invalid
            else:
                shipping_distance = 1000  # Default

            shipping_factor = self._get_shipping_factor(shipping_distance)
            shipping_emission = shipping_distance * shipping_factor

            # Safe access to all dictionary values
            volume_key = input_df["shipping_volume"].iloc[0]
            volume_factor = self.shipping_volume_factors.get(volume_key, 1.0) if volume_key else 1.0
            shipping_emission *= volume_factor

            # Material emission
            material_key = input_df["raw_material"].iloc[0]
            material_emission = self.material_emissions.get(material_key, 2.0) if material_key else 2.0

            # Embedded material emission
            embedded_key = input_df["embedded_material"].iloc[0]
            craft_type = input_df["craft_type"].iloc[0]
            is_papier_mache = craft_type == "Papier-Mâché Items" if craft_type else False
            embedded_emission = self.embedded_material_emissions.get(embedded_key, 0.0) if embedded_key and is_papier_mache else 0.0

            # Processing emission
            processing_key = input_df["processing"].iloc[0]
            processing_emission = self.production_emissions.get(processing_key, 1.5) if processing_key else 1.5

            # Crafting emission
            crafting_key = input_df["crafting"].iloc[0]
            crafting_emission = self.dye_emissions.get(crafting_key, 0.0) if crafting_key else 0.0

            # Special handling for Embroidery category - no packaging
            craft_category = input_df["craft_category"].iloc[0]
            if craft_category == "Embroidery":
                packaging_emission = 0.0
            else:
                # Packaging emission
                packaging_key = input_df["packaging"].iloc[0]
                packaging_emission = self.packaging_emissions.get(packaging_key, 1.0) if packaging_key else 1.0

            # Transportation emission
            transportation_key = input_df["transportation"].iloc[0]
            transportation_emission = self.transportation_emissions.get(transportation_key, 2.0) if transportation_key else 2.0

            # Certification emission
            certification_key = input_df["certifications"].iloc[0]
            certification_emission = self.certification_emissions.get(certification_key, 0.0) if certification_key else 0.0

            # Weaving emission
            weaving_key = input_df["weaving_design"].iloc[0]
            weaving_applicable_types = ["Pashmina", "Cashmere", "Silk", "Kashmiri Bags and Purses", "Kashmiri Jackets", "Kaftans", "Kurtas", "Pherans", "Kashmiri Jewelry"]
            is_weaving_type = craft_type in weaving_applicable_types if craft_type else False
            weaving_emission = self.weaving_emissions.get(weaving_key, 0.0) if weaving_key and is_weaving_type else 0.0

            # Finishing emission
            finishing_key = input_df["finishing_technique"].iloc[0]
            finishing_applicable_types = ["Papier-Mâché Items", "Tapestry", "Jeweled Wall Hangings", "Office Accessories", "Room Divider Screens", "Sofa and Cushion Covers", "Bed Linens", "Kashmiri Jewelry"]
            is_finishing_type = craft_type in finishing_applicable_types if craft_type else False
            finishing_emission = self.dye_emissions.get(finishing_key, 0.0) if finishing_key and is_finishing_type else 0.0

            # Fabric choice emission
            fabric_choice_emission = 0
            if "fabric_choice" in input_df.columns and input_df["fabric_choice"].iloc[0]:
                fabric_choice = str(input_df["fabric_choice"].iloc[0])
                if "Pashmina" in fabric_choice:
                    fabric_choice_emission = 2.5
                elif "Silk" in fabric_choice:
                    fabric_choice_emission = 4.0
                elif "Velvet" in fabric_choice:
                    fabric_choice_emission = 3.8
                elif "Cotton" in fabric_choice:
                    fabric_choice_emission = 1.8
                elif "Wool" in fabric_choice:
                    fabric_choice_emission = 3.0
                else:
                    fabric_choice_emission = 2.0

            # Calculate total emission
            total_emission = (
                material_emission +
                embedded_emission +
                processing_emission +
                crafting_emission +
                packaging_emission +
                transportation_emission +
                shipping_emission +
                certification_emission +
                weaving_emission +
                finishing_emission + 
                fabric_choice_emission
            )

            # Generate recommendations
            recommendations, explanations = self._generate_detailed_recommendations(
                input_data, predictions, total_emission
            )

            # Calculate confidence level
            unknown_count = sum(1 for value in input_data.dict().values() if value == "I don't know" or value is None)
            confidence_level = self._get_confidence_level(unknown_count)

            # Return results
            return {
                "carbon_footprint": round(total_emission, 2),
                "unit": "kg CO2e",
                "confidence_level": confidence_level,
                "recommendations": recommendations,
                "explanations": explanations,
                "breakdown": {
                    "raw_material": round(material_emission, 2),
                    "embedded_material": round(embedded_emission, 2),
                    "fabric_choice": round(fabric_choice_emission, 2),
                    "processing": round(processing_emission, 2),
                    "crafting": round(crafting_emission, 2),
                    "packaging": round(packaging_emission, 2),
                    "transportation": round(transportation_emission, 2),
                    "shipping": round(shipping_emission, 2),
                    "certifications": round(certification_emission, 2),
                    "weaving": round(weaving_emission, 2),
                    "finishing": round(finishing_emission, 2)
                }
            }
        except Exception as e:
            raise ValueError(f"Error calculating carbon footprint: {str(e)}")

    def _get_shipping_factor(self, distance: float) -> float:
        if distance <= self.shipping_categories["local"]["max_distance"]:
            return self.shipping_categories["local"]["factor"]
        elif distance <= self.shipping_categories["regional"]["max_distance"]:
            return self.shipping_categories["regional"]["factor"]
        else:
            return self.shipping_categories["international"]["factor"]

    def _get_confidence_level(self, unknown_count: int) -> str:
        if unknown_count == 0:
            return "high"
        elif unknown_count <= 2:
            return "medium"
        else:
            return "low"