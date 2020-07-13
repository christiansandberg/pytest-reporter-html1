
function init() {
    var selectElements = document.getElementsByClassName("category-select");
    Array.prototype.forEach.call(selectElements, function(el) {
        var category = el.dataset.category;
        var categoryElements = document.getElementsByClassName(category);
        el.addEventListener("click", function(e) {
            // var someHidden = Array.prototype.some.call(selectElements, function(el) {
            //     return el.classList.contains("hidden");
            // });
            // if (!someHidden) {
            //     Array.prototype.forEach.call(selectElements, function(el) {
            //         el.classList.add("hidden");
            //     });
            //     // Array.prototype.forEach.call(categoryElements, function(el) {
            //     //     el.classList.add("hidden");
            //     // });
            // }

            var hidden = el.classList.toggle("hidden");
            Array.prototype.forEach.call(categoryElements, function(el) {
                el.classList.toggle("hidden", hidden);
            });

            // var allHidden = Array.prototype.every.call(selectElements, function(el) {
            //     return el.classList.contains("hidden");
            // });
            // if (allHidden) {
            //     var hiddenElements = document.getElementsByClassName("hidden");
            //     Array.prototype.forEach.call(hiddenElements, function(el) {
            //         el.classList.remove("hidden");
            //     });
            // }
        });
    });
}

window.onload = init;
