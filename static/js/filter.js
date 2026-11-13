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

// bu kod ancaq secil secilen nesil gosterilecel

document.addEventListener("DOMContentLoaded", function () {
    const modelSelect = document.querySelector('select[name="model"]'); 
    const genSelect = document.getElementById('generation-select');
    const genOptions = genSelect.querySelectorAll('option[data-model]');

    function updateGenerations() {
        const selectedModelId = modelSelect.value;
        
        // ereset 
        if (!selectedModelId) {
            genSelect.value = "";
            genSelect.disabled = true;
            genSelect.options[0].textContent = "Əvvəlcə model seçin (Nəsil ✨)";
            genOptions.forEach(opt => opt.style.display = "none");
            return;
        }

        let matchCount = 0;
        genOptions.forEach(opt => {
            if (opt.getAttribute('data-model') === selectedModelId) {
                opt.style.display = "block";
                matchCount++;
            } else {
                opt.style.display = "none";
            }
        });

        if (matchCount > 0) {
            genSelect.disabled = false;
            genSelect.options[0].textContent = "Nəsil (YENİ ✨)";
        } else {
            // 
            genSelect.value = "";
            genSelect.disabled = true;
            genSelect.options[0].textContent = "Nəsil yoxdur";
        }
    }

    if (modelSelect && genSelect) {
        modelSelect.addEventListener('change', function () {
            genSelect.value = "";
            updateGenerations();
        });
        // bidende tun olacaq 
        updateGenerations();
    }
});
