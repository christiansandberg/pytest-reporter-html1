
function collapse() {
    var elements = document.getElementsByClassName('collapsible');
    Array.prototype.forEach.call(elements, function(el) {
        el.classList.add('collapsed');
        el.querySelector(':scope > .title').addEventListener('click', function() {
            el.classList.toggle('collapsed');
        });
    });
}

window.onload = function() {
    collapse();
}
