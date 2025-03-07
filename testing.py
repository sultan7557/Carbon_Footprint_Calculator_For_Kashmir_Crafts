main_categories = [
    "Weaving Crafts",
    "Embroidery Craft",
    "Wood Crafts",
    "Wicker Crafts",
    "Sport Crafts",
    "Hide Crafts",
    "Culinary Weaving",
    "Recycled Crafts"
]

subcategories = {
    "Weaving Crafts": ["Pashmina Shawl", "Kani Shawl", "Silk", "Carpet"],
    "Embroidery Craft": ["Embroidery craft"],
    "Wood Crafts": ["Walnut Wood Carving Furniture", "Khatamband", "Pinjrakari"],
    "Wicker Crafts": ["Wicker"],
    "Sport Crafts": ["Cricket Bat Making", "Chess Board Making"],
    "Hide Crafts": ["Leather Craft", "Fur Astrakhan Craft"],
    "Culinary Weaving": ["Wazwan", "Kahwa Pink Tea"],
    "Recycled Crafts": ["Papier Mache", "Gabba"]
}

# Raw Materials
material_emissions = {
    # Weaving Crafts
    "Pure Pashmina (100%)": 2.5, "Pashmina-Silk Blend": 4.5, "Pashmina-Wool Blend": 4.5, "Synthetic Blend": 6.5,
    "Pure (Pashmina)": 2.5, "Pure Silk": 5.0, "Silk-Pashmina Blend": 4.0, "Silk-Cotton Blend": 3.5, "Synthetic Silk Blend": 6.0,
    "Silk on Silk": 6.0, "Silk on Cotton": 5.0, "Cotton on Cotton": 3.5, "Cotton on Wool": 4.5,
    # Embroidery Craft
    "Pure Cotton Base": 2.5, "Silk Base": 3.5, "Wool Base": 4.5, "Synthetic Base": 6.0,
    # Wood Crafts
    "Pure Walnut Wood": 6.0, "Walnut with MDF Base": 5.0, "Synthetic/Composite Wood": 7.5,
    # Wicker Crafts
    "Pure Wool": 3.5, "Wool-Cotton Blend": 4.0,
    # Sport Crafts
    "Willow Wood": 4.0, "Willow with Synthetic Handle": 5.0, "Synthetic Composite": 6.0,
    "Synthetic/Composite Material": 5.5,
    # Hide Crafts
    "Pure Leather": 5.0, "Leather with Synthetic Components": 4.0, "Synthetic Leather": 6.0,
    "Pure Astrakhan Fur": 7.0, "Fur-Synthetic Blend": 5.0, "Synthetic Fur": 4.0,
    # Culinary Weaving
    "Local Ingredients": 3.5, "Non-Local Ingredients": 5.5, "Imported Ingredients": 8.5,
    # Recycled Crafts
    "Recycled Paper Base": 2.5, "Recycled Paper with Wood Base": 3.5, "Recycled Wool Base": 2.5
}

# Processing Emissions (nested, using midpoints)
processing_emissions = {
    # Weaving Crafts - Pashmina Shawl, Kani Shawl
    "Wool Cleaning": {"Pure Pashmina (100%)": 1.0, "Pashmina-Silk Blend": 1.25, "Pashmina-Wool Blend": 1.25, "Synthetic Blend": 2.25},
    "Spinning": {"Pure Pashmina (100%)": 0.75, "Pashmina-Silk Blend": 2.0, "Pashmina-Wool Blend": 2.0, "Synthetic Blend": 2.5},
    "Dyeing (Natural)": {"Pure Pashmina (100%)": 0.5, "Pashmina-Silk Blend": 0.75, "Pashmina-Wool Blend": 0.75, "Synthetic Blend": 0.0},
    "Dyeing (Synthetic)": {"Pure Pashmina (100%)": 0.0, "Pashmina-Silk Blend": 1.25, "Pashmina-Wool Blend": 1.25, "Synthetic Blend": 2.25},
    # Weaving Crafts - Silk
    "Sericulture (Mulberry Farming)": {"Pure Silk": 2.5, "Silk-Pashmina Blend": 1.5, "Silk-Cotton Blend": 1.5, "Synthetic Silk Blend": 0.0},
    # Weaving Crafts - Carpet
    "Material Cleaning": {"Silk on Silk": 1.75, "Silk on Cotton": 1.25, "Cotton on Cotton": 1.25, "Cotton on Wool": 1.5, "Synthetic Blend": 2.25},
    # Embroidery Craft
    "Base Preparation (Manual)": {"Pure Cotton Base": 0.75, "Silk Base": 1.25, "Wool Base": 1.75, "Synthetic Base": 0.0},
    "Base Preparation (Machine)": {"Pure Cotton Base": 1.25, "Silk Base": 1.75, "Wool Base": 2.5, "Synthetic Base": 3.5},
    # Wood Crafts
    "Wood Harvesting": {"Pure Walnut Wood": 2.5, "Walnut with MDF Base": 2.0, "Synthetic/Composite Wood": 2.75},
    "Drying (Natural)": {"Pure Walnut Wood": 1.25, "Walnut with MDF Base": 0.75, "Synthetic/Composite Wood": 0.0},
    "Drying (Kiln)": {"Pure Walnut Wood": 2.5, "Walnut with MDF Base": 2.0, "Synthetic/Composite Wood": 2.5},
    "Surface Finishing (Manual)": {"Pure Walnut Wood": 0.75, "Walnut with MDF Base": 0.75, "Synthetic/Composite Wood": 0.0},
    "Surface Finishing (Machine)": {"Pure Walnut Wood": 0.0, "Walnut with MDF Base": 1.25, "Synthetic/Composite Wood": 1.75},
    # Wicker Crafts
    "Wool Cleaning (Manual)": {"Pure Wool": 0.75, "Wool-Cotton Blend": 0.75, "Synthetic Blend": 0.0},
    "Wool Cleaning (Machine)": {"Pure Wool": 1.25, "Wool-Cotton Blend": 1.25, "Synthetic Blend": 2.5},
    "Blending (Manual)": {"Pure Wool": 0.75, "Wool-Cotton Blend": 0.75, "Synthetic Blend": 0.0},
    "Blending (Machine)": {"Pure Wool": 1.25, "Wool-Cotton Blend": 1.25, "Synthetic Blend": 2.5},
    # Sport Crafts - Cricket Bat
    "Wood Harvesting (Manual)": {"Willow Wood": 1.5, "Willow with Synthetic Handle": 2.0, "Synthetic Composite": 0.0},
    "Wood Harvesting (Machine)": {"Willow Wood": 2.5, "Willow with Synthetic Handle": 3.0, "Synthetic Composite": 3.5},
    "Handle Assembly (Manual)": {"Willow Wood": 0.75, "Willow with Synthetic Handle": 1.0, "Synthetic Composite": 0.0},
    "Handle Assembly (Machine)": {"Willow Wood": 1.25, "Willow with Synthetic Handle": 1.5, "Synthetic Composite": 2.5},
    # Sport Crafts - Chess Board
    "Base Preparation (Manual)": {"Walnut Wood": 0.75, "Walnut with MDF Base": 0.75, "Synthetic/Composite Material": 0.0},
    "Base Preparation (Machine)": {"Walnut Wood": 1.25, "Walnut with MDF Base": 1.25, "Synthetic/Composite Material": 2.5},
    # Hide Crafts - Leather
    "Tanning (Vegetable-Based)": {"Pure Leather": 2.5, "Leather with Synthetic Components": 2.0, "Synthetic Leather": 0.0},
    "Tanning (Chemical-Based)": {"Pure Leather": 0.0, "Leather with Synthetic Components": 2.5, "Synthetic Leather": 3.5},
    # Hide Crafts - Fur Astrakhan
    "Fur Preparation (Manual)": {"Pure Astrakhan Fur": 2.5, "Fur-Synthetic Blend": 2.0, "Synthetic Fur": 0.0},
    "Fur Preparation (Machine)": {"Pure Astrakhan Fur": 3.5, "Fur-Synthetic Blend": 3.0, "Synthetic Fur": 2.5},
    # Culinary Weaving - Wazwan
    "Traditional Cooking": {"Local Ingredients": 2.5, "Non-Local Ingredients": 3.25, "Imported Ingredients": 4.0},
    "Modern Cooking": {"Local Ingredients": 1.5, "Non-Local Ingredients": 2.25, "Imported Ingredients": 3.0},
    "Cooking Process": {"Local Ingredients": 2.5, "Non-Local Ingredients": 3.5, "Imported Ingredients": 5.0},
    # Culinary Weaving - Kahwa Pink Tea
    "Traditional Brewing": {"Local Ingredients": 1.5, "Non-Local Ingredients": 2.25, "Imported Ingredients": 2.75},
    "Modern Brewing (Electric)": {"Local Ingredients": 0.75, "Non-Local Ingredients": 1.25, "Imported Ingredients": 2.0},
    "Additives (Spices, Nuts)": {"Local Ingredients": 1.25, "Non-Local Ingredients": 2.5, "Imported Ingredients": 3.5},
    # Recycled Crafts - Papier Mache
    "Pulp Preparation (Manual)": {"Recycled Paper Base": 0.75, "Recycled Paper with Wood Base": 0.75, "Synthetic Base": 0.0},
    "Pulp Preparation (Machine)": {"Recycled Paper Base": 1.25, "Recycled Paper with Wood Base": 1.25, "Synthetic Base": 2.5},
    # Recycled Crafts - Gabba
    "Material Cleaning (Manual)": {"Recycled Wool Base": 0.75, "Wool-Cotton Blend": 0.75, "Synthetic Blend": 0.0},
    "Material Cleaning (Machine)": {"Recycled Wool Base": 1.25, "Wool-Cotton Blend": 1.25, "Synthetic Blend": 2.5}
}

# Crafting Emissions
crafting_emissions = {
    # Weaving Crafts - Pashmina Shawl
    "Hand Weaving": {"Pure Pashmina (100%)": 0.75, "Pashmina-Silk Blend": 1.25, "Pashmina-Wool Blend": 1.25, "Synthetic Blend": 2.5},
    "Handloom Weaving": {"Pure Pashmina (100%)": 1.75, "Pashmina-Silk Blend": 2.25, "Pashmina-Wool Blend": 2.25, "Synthetic Blend": 3.5},
    "Mass Production": {"Pure Pashmina (100%)": 0.0, "Pashmina-Silk Blend": 5.0, "Pashmina-Wool Blend": 5.5, "Synthetic Blend": 6.5},
    # Weaving Crafts - Kani Shawl
    "Kani Weaving": {"Pure (Pashmina)": 2.5, "Pashmina-Silk Blend": 3.5, "Pashmina-Wool Blend": 3.5, "Synthetic Blend": 4.5},
    "Complexity (Simple)": {"Pure (Pashmina)": 1.25, "Pashmina-Silk Blend": 1.75, "Pashmina-Wool Blend": 1.75, "Synthetic Blend": 2.5},
    "Complexity (Intricate)": {"Pure (Pashmina)": 2.5, "Pashmina-Silk Blend": 3.0, "Pashmina-Wool Blend": 3.0, "Synthetic Blend": 3.75},
    # Weaving Crafts - Silk
    "Handloom Weaving": {"Pure Silk": 1.5, "Silk-Pashmina Blend": 2.5, "Silk-Cotton Blend": 2.0, "Synthetic Silk Blend": 3.5},
    "Machine Weaving": {"Pure Silk": 2.5, "Silk-Pashmina Blend": 3.5, "Silk-Cotton Blend": 3.0, "Synthetic Silk Blend": 4.5},
    # Weaving Crafts - Carpet
    "Hand-Knotting (Simple)": {"Silk on Silk": 4.5, "Silk on Cotton": 3.5, "Cotton on Cotton": 2.5, "Cotton on Wool": 3.5, "Synthetic Blend": 5.5},
    "Hand-Knotting (Intricate)": {"Silk on Silk": 7.0, "Silk on Cotton": 5.5, "Cotton on Cotton": 4.5, "Cotton on Wool": 5.5, "Synthetic Blend": 8.0},
    "Machine-Knotting (Mass Production)": {"Silk on Silk": 9.0, "Silk on Cotton": 7.5, "Cotton on Cotton": 6.5, "Cotton on Wool": 7.5, "Synthetic Blend": 9.5},
    # Embroidery Craft
    "Sozni Embroidery (Simple)": {"Pure Cotton Base": 2.5, "Silk Base": 3.0, "Wool Base": 3.5, "Synthetic Base": 4.5},
    "Sozni Embroidery (Intricate)": {"Pure Cotton Base": 3.5, "Silk Base": 4.0, "Wool Base": 4.5, "Synthetic Base": 5.5},
    "Aari Work (Simple)": {"Pure Cotton Base": 1.5, "Silk Base": 2.5, "Wool Base": 3.5, "Synthetic Base": 4.5},
    "Aari Work (Intricate)": {"Pure Cotton Base": 2.5, "Silk Base": 3.5, "Wool Base": 4.5, "Synthetic Base": 5.5},
    # Wood Crafts
    "Hand Carving (Simple)": {"Pure Walnut Wood": 3.5, "Walnut with MDF Base": 2.5, "Synthetic/Composite Wood": 3.5},
    "Hand Carving (Intricate)": {"Pure Walnut Wood": 5.5, "Walnut with MDF Base": 4.5, "Synthetic/Composite Wood": 5.5},
    "Machine-Assisted Carving": {"Pure Walnut Wood": 4.5, "Walnut with MDF Base": 3.5, "Synthetic/Composite Wood": 4.5},
    "Hand Assembly (Simple Patterns)": {"Pure Walnut Wood": 3.5, "Walnut with MDF Base": 2.5, "Synthetic/Composite Wood": 3.5},
    "Hand Assembly (Intricate Patterns)": {"Pure Walnut Wood": 5.5, "Walnut with MDF Base": 4.5, "Synthetic/Composite Wood": 5.5},
    "Machine-Assisted Assembly": {"Pure Walnut Wood": 4.5, "Walnut with MDF Base": 3.5, "Synthetic/Composite Wood": 4.5},
    # Wicker Crafts
    "Hand Felting (Simple)": {"Pure Wool": 2.5, "Wool-Cotton Blend": 2.0, "Synthetic Blend": 3.5},
    "Hand Felting (Intricate)": {"Pure Wool": 3.5, "Wool-Cotton Blend": 3.0, "Synthetic Blend": 4.5},
    "Machine-Assisted Felting": {"Pure Wool": 4.5, "Wool-Cotton Blend": 3.5, "Synthetic Blend": 5.5},
    # Sport Crafts
    "Hand Shaping (Simple)": {"Willow Wood": 1.5, "Willow with Synthetic Handle": 2.0, "Synthetic Composite": 2.5},
    "Hand Shaping (Intricate)": {"Willow Wood": 2.5, "Willow with Synthetic Handle": 3.0, "Synthetic Composite": 3.5},
    "Machine-Assisted Shaping": {"Willow Wood": 3.5, "Willow with Synthetic Handle": 3.5, "Synthetic Composite": 4.5},
    # Hide Crafts
    "Hand Stitching (Simple)": {"Pure Leather": 1.5, "Leather with Synthetic Components": 2.0, "Synthetic Leather": 2.5},
    "Hand Stitching (Intricate)": {"Pure Leather": 2.5, "Leather with Synthetic Components": 3.0, "Synthetic Leather": 3.5},
    "Machine-Assisted Stitching": {"Pure Leather": 3.5, "Leather with Synthetic Components": 3.5, "Synthetic Leather": 4.5},
    "Hand Tailoring (Simple)": {"Pure Astrakhan Fur": 1.5, "Fur-Synthetic Blend": 2.0, "Synthetic Fur": 2.5},
    "Hand Tailoring (Intricate)": {"Pure Astrakhan Fur": 2.5, "Fur-Synthetic Blend": 3.0, "Synthetic Fur": 3.5},
    "Machine-Assisted Tailoring": {"Pure Astrakhan Fur": 3.5, "Fur-Synthetic Blend": 3.5, "Synthetic Fur": 4.5},
    # Recycled Crafts
    "Hand Molding (Simple)": {"Recycled Paper Base": 1.5, "Recycled Paper with Wood Base": 2.0, "Synthetic Base": 2.5},
    "Hand Molding (Intricate)": {"Recycled Paper Base": 2.5, "Recycled Paper with Wood Base": 3.0, "Synthetic Base": 3.5},
    "Machine-Assisted Molding": {"Recycled Paper Base": 3.5, "Recycled Paper with Wood Base": 3.5, "Synthetic Base": 4.5}
}

# Additional Crafting (e.g., Finishing, Painting)
additional_crafting_emissions = {
    # Sport Crafts
    "Polishing (Manual)": {"Willow Wood": 0.75, "Willow with Synthetic Handle": 0.75, "Synthetic Composite": 0.0, "Walnut Wood": 0.75, "Walnut with MDF Base": 0.75, "Synthetic/Composite Material": 0.0},
    "Polishing (Machine)": {"Willow Wood": 1.25, "Willow with Synthetic Handle": 1.25, "Synthetic Composite": 1.75, "Walnut Wood": 1.25, "Walnut with MDF Base": 1.25, "Synthetic/Composite Material": 1.75},
    # Hide Crafts
    "Polishing (Manual)": {"Pure Leather": 0.75, "Leather with Synthetic Components": 0.75, "Synthetic Leather": 0.0, "Pure Astrakhan Fur": 0.75, "Fur-Synthetic Blend": 0.75, "Synthetic Fur": 0.0},
    "Polishing (Machine)": {"Pure Leather": 1.25, "Leather with Synthetic Components": 1.25, "Synthetic Leather": 1.75, "Pure Astrakhan Fur": 1.25, "Fur-Synthetic Blend": 1.25, "Synthetic Fur": 1.75},
    # Recycled Crafts - Papier Mache
    "Hand Painting (Simple)": {"Recycled Paper Base": 1.25, "Recycled Paper with Wood Base": 1.75, "Synthetic Base": 2.25},
    "Hand Painting (Intricate)": {"Recycled Paper Base": 2.5, "Recycled Paper with Wood Base": 3.0, "Synthetic Base": 3.5},
    # Recycled Crafts - Gabba
    "Crewel Embroidery (Simple)": {"Recycled Wool Base": 1.25, "Wool-Cotton Blend": 1.75, "Synthetic Blend": 2.25},
    "Crewel Embroidery (Intricate)": {"Recycled Wool Base": 2.5, "Wool-Cotton Blend": 3.0, "Synthetic Blend": 3.5}
}

# Installation Emissions (for Khatamband)
installation_emissions = {
    "Local Installation": {"Pure Walnut Wood": 2.5, "Walnut with MDF Base": 2.0, "Synthetic/Composite Wood": 2.5},
    "Remote Installation": {"Pure Walnut Wood": 4.0, "Walnut with MDF Base": 3.25, "Synthetic/Composite Wood": 4.25}
}

# Packaging Emissions
packaging_emissions = {
    "Basic": {"Pure Pashmina (100%)": 0.5, "Pashmina-Silk Blend": 0.75, "Pashmina-Wool Blend": 0.75, "Synthetic Blend": 1.25},
    "Luxury (Papier-Mâché)": {"Pure Pashmina (100%)": 2.0, "Pashmina-Silk Blend": 2.25, "Pashmina-Wool Blend": 2.25, "Synthetic Blend": 2.5},
    "Plastic": {"Pure Pashmina (100%)": 1.25, "Pashmina-Silk Blend": 1.25, "Pashmina-Wool Blend": 1.25, "Synthetic Blend": 1.5},
    "Basic (Paper/Cloth)": {"Pure Cotton Base": 0.5, "Silk Base": 0.75, "Wool Base": 1.0, "Synthetic Base": 1.25},
    "Luxury (Eco-Friendly)": {"Pure Cotton Base": 1.25, "Silk Base": 1.5, "Wool Base": 1.75, "Synthetic Base": 2.5},
    "Basic (Cardboard)": {"Pure Walnut Wood": 1.0, "Walnut with MDF Base": 1.25, "Synthetic/Composite Wood": 1.25},
    "Luxury (Wooden Box)": {"Pure Walnut Wood": 2.5, "Walnut with MDF Base": 2.5, "Synthetic/Composite Wood": 2.5},
    "Basic (Plastic Wrap)": {"Willow Wood": 0.75, "Willow with Synthetic Handle": 0.75, "Synthetic Composite": 1.25}
}

# Transportation Emissions
transportation_emissions = {
    "Local": {"Pure Pashmina (100%)": 0.75, "Pashmina-Silk Blend": 1.0, "Pashmina-Wool Blend": 1.0, "Synthetic Blend": 1.5},
    "Domestic": {"Pure Pashmina (100%)": 1.5, "Pashmina-Silk Blend": 2.0, "Pashmina-Wool Blend": 2.0, "Synthetic Blend": 2.5},
    "International (Air)": {"Pure Pashmina (100%)": 6.0, "Pashmina-Silk Blend": 6.0, "Pashmina-Wool Blend": 6.0, "Synthetic Blend": 7.0},
    "International (Sea)": {"Pure Pashmina (100%)": 2.5, "Pashmina-Silk Blend": 3.0, "Pashmina-Wool Blend": 3.0, "Synthetic Blend": 3.5},
    "Bulk Shipping (Sea)": {"Pure Pashmina (100%)": 1.0, "Pashmina-Silk Blend": 1.5, "Pashmina-Wool Blend": 1.5, "Synthetic Blend": 2.5}
}