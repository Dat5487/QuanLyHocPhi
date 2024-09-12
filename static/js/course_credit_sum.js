window.addEventListener('DOMContentLoaded', function() {
{% for course in courses %}
    {% for selected_course in selected_courses %}
    if ("{{ course }}" == "{{ selected_course }}") {
        var checkbox = document.getElementById("a{{ course.id }}");
        checkbox.checked = true;
    }
    {% endfor %}
{% endfor %}
updateSum();
});
    function updateSum() {
    var checkboxes = document.getElementsByName('course');
    var sum = 0;

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            {% for course in courses %}
            if ("{{ course.id }}" == checkboxes[i].value) {
                sum += parseInt("{{ course.payment_amount }}");
            }
            {% endfor %}
        
        }
    }
    updateSumCredit();
    document.getElementById('total_payment_amount').textContent = sum.toLocaleString() + " (" + to_vietnamese(sum).charAt(0).toUpperCase() + to_vietnamese(sum).slice(1) + ")";
    }
    function updateSumCredit() {
    var checkboxes = document.getElementsByName('course');
    var sum = 0;

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            {% for course in courses %}
            if ("{{ course.id }}" == checkboxes[i].value) {
                sum += parseInt("{{ course.course_credit }}");
            }
            {% endfor %}
        }
    }
    document.getElementById('total_course_credit').textContent = sum.toLocaleString();
}
