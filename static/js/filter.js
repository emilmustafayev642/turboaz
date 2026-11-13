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

// BU KOD ANCAQ SECILEN NESILIN SEKILLERINI GOSTERIR

function clearSelectedGeneration() {
    const genLabel = document.getElementById('selected-generation-label');
    if (genLabel) genLabel.innerText = 'Nəsil (YENİ ✨)';
    document.querySelectorAll('#index-generations-grid input[name="generation"]').forEach(radio => {
        radio.checked = false;
    });
}

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

        selectedBrandLabel.textContent = brandSelect.value || 'Marka';
        selectedModelLabel.textContent = 'Model';
        modelSelect.replaceChildren(new Option('Model', '', true, true));
        modelSelect.disabled = models.length === 0;

        models.forEach((model) => {
            modelSelect.add(new Option(model, model));
        });

        // Reset onurun brand deyisilende
        clearSelectedGeneration();
    });

    modelSelect.addEventListener('change', () => {
        selectedModelLabel.textContent = modelSelect.value || 'Model';
        // Reset onurun model deyisilende
        clearSelectedGeneration();
    });
});

// burda imneno duzgun masinin generations gosterir 


function toggleGenDropdown(event) {
    event.stopPropagation();
    const menu = document.getElementById('genDropdownMenu');
    const modelSelect = document.getElementById('model-select');
    const selectedModel = modelSelect ? modelSelect.value.trim() : '';
    const cards = document.querySelectorAll('#index-generations-grid .gen-card');
    const emptyMsg = document.getElementById('gen-empty-msg');

    let matchCount = 0;

    // Yalnız seçilən modelin generation-larını göstəririk
    cards.forEach(card => {
        if (selectedModel && card.dataset.modelName.trim() === selectedModel) {
            card.style.display = 'block';
            matchCount++;
        } else {
            card.style.display = 'none';
        }
    });

    if (emptyMsg) {
        if (!selectedModel) {
            emptyMsg.textContent = 'Əvvəlcə marka və model seçin';
            emptyMsg.style.display = 'block';
        } else if (matchCount === 0) {
            emptyMsg.textContent = 'Bu model üçün nəsil əlavə edilməyib';
            emptyMsg.style.display = 'block';
        } else {
            emptyMsg.style.display = 'none';
        }
    }

    menu.classList.toggle('show');
}

function selectGenCard(genName) {
    document.getElementById('selected-generation-label').innerText = genName;
    const menu = document.getElementById('genDropdownMenu');
    if (menu) menu.classList.remove('show');
}

// sehideni baglayiriq basand a
document.addEventListener('click', function() {
    const menu = document.getElementById('genDropdownMenu');
    if (menu) menu.classList.remove('show');
});



const resetButton = document.getElementById('hard-reset-btn');
resetButton.addEventListener('click', function(event) {
    event.preventDefault();
    window.location.assign(resetButton.form.action);
});


