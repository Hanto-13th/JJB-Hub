const checkboxes = document.querySelectorAll('input[name="drill_check"]');
const deleteBtn = document.querySelector('button[value="delete"]');
const accomplishBtn = document.querySelector('button[value="accomplish"]');

function updateButtons() {
    //check if at least one checkbox is checked
    const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
    deleteBtn.disabled = !anyChecked;
    accomplishBtn.disabled = !anyChecked;
    //if one is checked at least the button is enabled to active
}

//listen all updates
checkboxes.forEach(cb => cb.addEventListener('change', updateButtons));