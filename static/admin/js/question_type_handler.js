function updateQuestionTypeFields() {
    document.querySelectorAll('.inline-related').forEach(group => {
        const typeSelect = group.querySelector('select[id$="-question_type"]');
        if (!typeSelect) return;
        
        group.dataset.questionType = typeSelect.value;
        
        typeSelect.addEventListener('change', function() {
            group.dataset.questionType = this.value;
        });
    });
}

document.addEventListener('DOMContentLoaded', updateQuestionTypeFields);
document.addEventListener('formset:added', updateQuestionTypeFields);