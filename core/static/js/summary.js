function scrollMenu(id) {
    window.scroll(
    {
        top: document.getElementById(id).getBoundingClientRect().top + window.scrollY - 180,
        behavior: 'smooth'
    }
);
}

document.getElementById("principal-content").querySelectorAll('h2, h3, h4').forEach((heading) => {
    if (heading.children.length == 1) {
        const anchorLink = document.createElement('a');

        anchorLink.classList.add(heading.tagName);

        anchorLink.textContent = heading.textContent;
        anchorLink.setAttribute('onclick', 'scrollMenu("' + heading.children[0].id + '")')

        const li = document.createElement('li')
        li.className = "list-group-item"
        li.appendChild(anchorLink);

        document.getElementById("sidebar-item").appendChild(li);
    }
});


if (document.getElementById("sidebar-item").children.length == 0) {
    document.getElementById("sidebar").remove();
}