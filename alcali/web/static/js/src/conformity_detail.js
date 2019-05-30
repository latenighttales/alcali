function panelState(name, color, states) {
  Object.keys(states).forEach(function (state, index) {
    let panelTemplate = document.getElementById('panelTemplate');
    let clonedTemplate = panelTemplate.cloneNode(true);
    clonedTemplate.style.display = "block";
    clonedTemplate.querySelector('.panel-heading').id = "heading" + name + index;
    clonedTemplate.querySelector('.panel-collapse').id = "collapse" + name + index;
    clonedTemplate.getElementsByTagName('a')[0].href = "#collapse" + name + index;
    clonedTemplate.getElementsByTagName('a')[0].innerText = state;
    clonedTemplate.getElementsByTagName('a')[0].classList.add("col-" + color);
    clonedTemplate.getElementsByTagName('a')[0].setAttribute("aria-controls", "collapse" + name + index);
    clonedTemplate.querySelector('.panel-collapse').setAttribute("aria-labelledby", "heading" + name + index);
    clonedTemplate.querySelector('.ansiStyle').innerHTML = states[state];

    panelTemplate.parentNode.appendChild(clonedTemplate);
  });
}

panelState("succeeded", "green", succeeded);
panelState("unchanged", "orange", unchanged);
panelState("failed", "red", failed);

/*htmlDetail.innerHTML += succeeded;
htmlDetail.innerHTML += unchanged;
htmlDetail.innerHTML += failed;*/
