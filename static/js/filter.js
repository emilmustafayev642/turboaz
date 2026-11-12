document.addEventListener('DOMContentLoaded', () => {
    const modelsByBrand = JSON.parse(
    document.getElementById('models-by-brand-data').textContent
    );

    const brandSelect = document.getElementById('brand-select');
    const modelSelect = document.getElementById('model-select');
    const selectedBrandLabel = document.getElementById('selected-brand-label');
    const selectedModelLabel = document.getElementById('selected-model-label');

    brandSelect.addEventListener('change', () => {
        const models = modelsByBrand[brandSelect.value] || [];

        selectedBrandLabel.textContent = brandSelect.value;
        selectedModelLabel.textContent = 'Model';
        modelSelect.replaceChildren(new Option('Model', '', true, true));
        modelSelect.disabled = models.length === 0;

        models.forEach((model) => {
            modelSelect.add(new Option(model, model));
        });
    });

    modelSelect.addEventListener('change', () => {
        selectedModelLabel.textContent = modelSelect.value;
    });
});


// burda imneno duzgun masinin generations gosterir 


function toggleGenDropdown(event) {
    event.stopPropagation();
    const menu = document.getElementById('genDropdownMenu');
    const modelSelect = document.getElementById('model-select');
    const selectedModel = modelSelect ? modelSelect.value : '';
    const cards = document.querySelectorAll('#index-generations-grid .gen-card');

    // secilen modelin generationun gosteririk
    cards.forEach(card => {
        if (!selectedModel || card.dataset.modelName === selectedModel) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });

    menu.classList.toggle('show');
}

function selectGenCard(genName) {
    document.getElementById('selected-generation-label').innerText = genName;
}

// sehideni baglayiriq basand a
document.addEventListener('click', function() {
    const menu = document.getElementById('genDropdownMenu');
    if (menu) menu.classList.remove('show');
});


// Reset filters and reload the unfiltered listing page.
const resetButton = document.getElementById('hard-reset-btn');
resetButton.addEventListener('click', function(event) {
    event.preventDefault();
    window.location.assign(resetButton.form.action);
});
