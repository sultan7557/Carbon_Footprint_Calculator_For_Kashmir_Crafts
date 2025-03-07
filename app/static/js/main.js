document.getElementById('calculatorForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value === "" ? null : value;
    }

    const mappedData = {
        main_category: data.main_category,
        subcategory: data.subcategory,
        craft_category: data.main_category,
        craft_type: data.subcategory,
        raw_material: data.raw_material,
        embedded_material: data.embedded_material,  // New field for Papier-Mâché
        processing: data.processing,
        crafting: data.crafting,
        certifications: data.certifications,
        weaving_design: data.weaving_design,
        finishing_technique: data.finishing_technique,
        shipping_distance: data.shipping_distance,
        shipping_volume: data.shipping_volume,
        shipping_location: data.shipping_location,
        dkc_warehouse: data.dkc_warehouse,
        packaging: data.packaging,
        transportation: data.transportation,
        quality: null,  // Optional fields not in form yet
        ply_type: null,
        embellishments: null,
        product_line_size: null
    };

    console.log('Sending data:', mappedData);

    try {
        const response = await fetch('/calculate-carbon-footprint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mappedData)
        });

        if (!response.ok) {
            const errorBody = await response.json();
            console.log('Validation error:', errorBody);
            const errorDetail = errorBody.detail || 'Unknown error';
            throw new Error(`Calculation failed: ${JSON.stringify(errorDetail)}`);
        }

        const result = await response.json();
        document.getElementById('result').classList.remove('hidden');
        const footprintElement = document.getElementById('footprint');
        footprintElement.textContent = `${result.carbon_footprint} ${result.unit}`;
        footprintElement.classList.toggle('text-green-600', result.carbon_footprint <= 10);
        footprintElement.classList.toggle('text-red-600', result.carbon_footprint > 10);
        document.getElementById('confidence').textContent = result.confidence_level;

        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = '';
        result.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recommendationsList.appendChild(li);
        });

        const explanationsList = document.getElementById('explanations');
        explanationsList.innerHTML = '';
        result.explanations.forEach(exp => {
            const li = document.createElement('li');
            li.textContent = exp;
            explanationsList.appendChild(li);
        });

        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();

    } catch (error) {
        console.error('Error:', error);
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();

        const errorDiv = document.createElement('div');
        errorDiv.className = 'mt-4 p-3 bg-red-50 text-red-700 rounded error-message';
        errorDiv.textContent = error.message || 'An error occurred while calculating the carbon footprint. Please try again.';
        document.getElementById('result').parentElement.appendChild(errorDiv);
    }
});