document.addEventListener('DOMContentLoaded', () => {
    const dataElement = document.getElementById('models-by-brand-data');
    const modelsByBrand = JSON.parse(dataElement.textContent);
    const brandTypes = JSON.parse(
        document.getElementById('brand-types-data').textContent
    );
    const bodyTypesByModel = JSON.parse(
        document.getElementById('body-types-by-model-data').textContent
    );
    const vehicleTypeInputs = document.querySelectorAll(
        'input[name="vehicle-type"]'
    );


    const years = JSON.parse(
        document.getElementById('years-data').textContent
    );
    const savedYear = JSON.parse(
        document.getElementById('selected-year-data').textContent
    );
    let selectedYear = null;

    
    const brandInput = document.getElementById('selected-brand-input');
    const modelInput = document.getElementById('selected-model-input');
    const clearBrandButton = document.getElementById('clear-brand-btn');
    const resetButton = document.getElementById('reset-form-btn');
    const modelInputBox = document.getElementById('model-input-box');
    const brandsSection = document.getElementById('brands-section');
    const modelsSection = document.getElementById('models-section');
    const brandsGrid = document.getElementById('popular-brands-grid');
    const modelsGrid = document.getElementById('models-grid');
    const yearGrid = document.getElementById('year-grid');
    const bodyTypeSelect = document.getElementById('id_body_type');

    function setBodyTypeChoices(modelId, selectedValue = '') {
        bodyTypeSelect.replaceChildren();
        const options = bodyTypesByModel[String(modelId)] || [];
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = options.length
            ? 'Ban növünü seçin'
            : 'Bu model üçün ban növü əlavə edilməyib';
        bodyTypeSelect.appendChild(placeholder);

        options.forEach((option) => {
            const element = document.createElement('option');
            element.value = option.value;
            element.textContent = option.label;
            bodyTypeSelect.appendChild(element);
        });
        bodyTypeSelect.value = selectedValue;
        bodyTypeSelect.disabled = options.length === 0;
        document.getElementById('body-type-help').textContent = options.length
            ? ''
            : 'Bu model üçün ban növü Admin panelində əlavə edilməyib.';
    }

    function clearBodyTypeChoices() {
        bodyTypeSelect.replaceChildren();
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Əvvəlcə model seçin';
        bodyTypeSelect.appendChild(placeholder);
        bodyTypeSelect.disabled = true;
        document.getElementById('body-type-help').textContent = '';
    }

    
    function renderChoices(
        container,
        choices,
        onSelect,
        getLabel = (choice) => choice
    ) 
    
    {
        container.replaceChildren();

        choices.forEach((choice) => {
            const button = document.createElement('button');
            button.type = 'button'; // Кнопка не будет отправлять форму.
            button.className = 'selection-option'; // Берём стиль кнопки из CSS.
            button.textContent = getLabel(choice);
            button.addEventListener('click', () => onSelect(choice)); // При нажатии выбираем вариант.
            container.appendChild(button); // Добавляем кнопку на страницу.
        });
    }

    // Запоминаем марку, показываем её модели и прячем список марок.
    function selectBrand(brandName) {
        brandInput.value = brandName;
        modelInput.value = '';
        clearBrandButton.hidden = false;
        modelInputBox.hidden = false;
        brandsSection.hidden = true;
        modelsSection.hidden = false;
        // Создаём кнопку для каждой модели этой марки.
        renderChoices(
            modelsGrid,
            modelsByBrand[brandName] || [], 
            (model) => {
            modelInput.value = model.name;
            document.getElementById('id_car_model').value = model.id;
            setBodyTypeChoices(model.id);
        },
        (model) => model.name
        );
    }

   
    function resetForm() {

        document.getElementById('id_car_model').value = '';
        document.getElementById('id_year').value = '';
        clearBodyTypeChoices();
        brandInput.value = '';
        modelInput.value = '';
        clearBrandButton.hidden = true;
        modelInputBox.hidden = true;
        brandsSection.hidden = false;
        modelsSection.hidden = true;
        selectedYear = null;
        yearGrid.querySelectorAll('.selection-option').forEach((button) => {
            button.classList.remove('is-selected');
            button.setAttribute('aria-pressed', 'false');
        });
    }

    function selectYear(year) {
        selectedYear = year;
        document.getElementById('id_year').value = year;

        yearGrid.querySelectorAll('.selection-option').forEach((button) => {
            const isSelected = Number(button.textContent) === year;
            button.classList.toggle('is-selected', isSelected);
            button.setAttribute('aria-pressed', String(isSelected));
        });
    }

    // При открытии страницы показываем все доступные марки.
    function updateBrandChoices(resetSelection = true) {
        const selectedType = document.querySelector(
            'input[name="vehicle-type"]:checked'
        ).value;

        const matchingBrands = Object.keys(modelsByBrand).filter(
            (brandName) => brandTypes[brandName] === selectedType
        );

        if (resetSelection) {
            resetForm();
        }
        renderChoices(brandsGrid, matchingBrands, selectBrand);
    }

    vehicleTypeInputs.forEach((input) => {
        input.addEventListener('change', () => updateBrandChoices(true));
    });

    const savedModelId = document.getElementById('id_car_model').value;
    const savedBodyType = bodyTypeSelect.value;
    updateBrandChoices(false);

    if (savedModelId) {
        const selectedBrand = Object.keys(modelsByBrand).find((brandName) =>
            modelsByBrand[brandName].some(
                (model) => String(model.id) === String(savedModelId)
            )
        );
        const selectedModel = selectedBrand
            ? modelsByBrand[selectedBrand].find(
                (model) => String(model.id) === String(savedModelId)
            )
            : null;

        if (selectedBrand && selectedModel) {
            brandInput.value = selectedBrand;
            modelInput.value = selectedModel.name;
            clearBrandButton.hidden = false;
            modelInputBox.hidden = false;
            brandsSection.hidden = true;
            modelsSection.hidden = false;
            renderChoices(
                modelsGrid,
                modelsByBrand[selectedBrand],
                (model) => {
                    modelInput.value = model.name;
                    document.getElementById('id_car_model').value = model.id;
                    setBodyTypeChoices(model.id);
                },
                (model) => model.name
            );
            setBodyTypeChoices(savedModelId, savedBodyType);
        }
    } else {
        clearBodyTypeChoices();
    }

    
    renderChoices(yearGrid, years, selectYear);
    if (savedYear) {
        selectYear(Number(savedYear));
    }


    
    clearBrandButton.addEventListener('click', resetForm);
    resetButton.addEventListener('click', resetForm);
});




const elanModelSelect = document.querySelector('[name="car_model"], #id_car_model, #model-select');
const elanBrandSelect = document.querySelector('[name="brand"], #id_brand, #brand-select');
const elanGenWrapper = document.getElementById('elan-generation-wrapper');
const elanGenCards = document.querySelectorAll('#elan-generations-grid .gen-card');

function filterElanGenerations() {
    if (!elanModelSelect || !elanGenWrapper) return;
    const selectedVal = elanModelSelect.value;

    // eger model secilmilbse nesili gizletirik murad muellim!!
    if (!selectedVal) {
        elanGenWrapper.style.display = 'none';
        elanGenCards.forEach(card => {
            card.style.display = 'none';
            const radio = card.querySelector('input[type="radio"]');
            if (radio) radio.checked = false;
        });
        return;
    }

    // model secildne sonra datadan nesilli axtatit
    let visibleCount = 0;
    elanGenCards.forEach(card => {
        if (card.dataset.modelId === selectedVal || card.dataset.modelName === selectedVal) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
            const radio = card.querySelector('input[type="radio"]');
            if (radio) radio.checked = false;
        }
    });

    // nesili gosterir acaq secilen modellerde 
    elanGenWrapper.style.display = visibleCount > 0 ? 'block' : 'none';
}

if (elanModelSelect) {
    elanModelSelect.addEventListener('change', filterElanGenerations);
    // yenilemeler c
    const observer = new MutationObserver(filterElanGenerations);
    observer.observe(elanModelSelect, { childList: true });
}

if (elanBrandSelect) {
    elanBrandSelect.addEventListener('change', () => {
        setTimeout(filterElanGenerations, 50);
    });
}

// start
filterElanGenerations();


// --- Nəsil (Pokoleniye) filtering by selected Model ---
(function () {
    const carModelHidden = document.getElementById('id_car_model');
    const selectedModelInput = document.getElementById('selected-model-input');
    const genWrapper = document.getElementById('elan-generation-wrapper');
    const genCards = document.querySelectorAll('#elan-generations-grid .gen-card');
    const noGenMsg = document.getElementById('no-generation-msg');

    let lastState = null;

    function updateGenerationsUI() {
        if (!genWrapper) return;

        const modelId = carModelHidden ? carModelHidden.value.trim() : '';
        const modelName = selectedModelInput ? selectedModelInput.value.trim().toLowerCase() : '';
        const currentState = modelId + '|' + modelName;

        if (currentState === lastState) return;
        lastState = currentState;

        // gizlet nesil maka ve model secilmemisden evvel
        if (!modelId && !modelName) {
            genWrapper.style.display = 'none';
            genCards.forEach(card => {
                card.style.display = 'none';
                const radio = card.querySelector('input[type="radio"]');
                if (radio) radio.checked = false;
            });
            return;
        }

        // 2. nesil goster secilen model ne maka ucun uygun
        genWrapper.style.display = 'block';
        let visibleCount = 0;

        genCards.forEach(card => {
            const cardModelId = card.dataset.modelId;
            const cardModelName = (card.dataset.modelName || '').toLowerCase();

            if ((modelId && cardModelId === modelId) || (modelName && cardModelName === modelName)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
                const radio = card.querySelector('input[type="radio"]');
                if (radio) radio.checked = false;
            }
        });

        if (noGenMsg) {
            noGenMsg.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }

    document.addEventListener('click', () => setTimeout(updateGenerationsUI, 30));
    setInterval(updateGenerationsUI, 250);
    updateGenerationsUI();
})();