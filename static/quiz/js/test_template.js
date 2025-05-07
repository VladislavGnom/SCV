document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('label > input[type="radio"]').forEach(radio => {
        radio.closest('label').classList.add('radio-option');
        let span_checkmark = document.createElement(tagName='span');
        span_checkmark.className = 'radio-checkmark';
        radio.closest('label').appendChild(span_checkmark)
    });
    document.querySelectorAll('label > input[type="checkbox"]').forEach(checkbox => {
        checkbox.closest('label').classList.add('checkbox-option');
        let span_checkmark = document.createElement(tagName='span');
        span_checkmark.className = 'checkbox-mark';
        checkbox.closest('label').appendChild(span_checkmark)
    });
})