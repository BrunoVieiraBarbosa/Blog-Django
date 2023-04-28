const TopY = document.getElementById('top').getBoundingClientRect().top + window.scrollY;
const projetosY = document.getElementById('projeto-concluido').getBoundingClientRect().top + window.scrollY - 70;
const PostsY = document.getElementById('posts-ultimos').getBoundingClientRect().top + window.scrollY;


document.getElementById('go-top').onclick = (event) => {
    window.scroll(
        {
            top: TopY,
            behavior: 'smooth'
        }
    );
}

document.getElementById('projetos').onclick = (event) => {
    console.log('ola');
    window.scroll(
        {
            top: projetosY,
            behavior: 'smooth'
        }
    );
}

document.getElementById('posts').onclick = (event) => {
    window.scroll(
        {
            top: PostsY,
            behavior: 'smooth'
        }
    );
}