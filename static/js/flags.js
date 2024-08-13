document.addEventListener('DOMContentLoaded', function () {
  const selectElement = document.getElementById('currencySelect');
  const options = selectElement.options;

  for (let i = 0; i < options.length; i++) {
    const option = options[i];
    const imgURL = option.getAttribute('data-image-url');
    if (imgURL) {
      option.style.backgroundImage = `url(${imgURL})`;
      option.style.backgroundRepeat = 'no-repeat';
      option.style.backgroundPosition = '10% 50%';
      option.style.backgroundSize = '20px';
      option.style.paddingLeft = '25px';
    }
  }

  selectElement.addEventListener('change', function () {
    const selectedOption = options[selectElement.selectedIndex];
    const imgURL = selectedOption.getAttribute('data-image-url');
    selectElement.style.backgroundImage = `url(${imgURL})`;
    selectElement.style.backgroundRepeat = 'no-repeat';
    selectElement.style.backgroundPosition = '10% 50%';
    selectElement.style.backgroundSize = '20px';
    selectElement.style.paddingLeft = '25px';
  });

  // Initialize the select element with the first option's image
  const initialOption = options[selectElement.selectedIndex];
  const initialImgURL = initialOption.getAttribute('data-image-url');
  selectElement.style.backgroundImage = `url(${initialImgURL})`;
  selectElement.style.backgroundRepeat = 'no-repeat';
  selectElement.style.backgroundPosition = '10% 50%';
  selectElement.style.backgroundSize = '20px';
  selectElement.style.paddingLeft = '25px';
});
