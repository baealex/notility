var gaButton = document.querySelector('.ga-form button');
gaButton && gaButton.addEventListener('click', function(e) {
    e.preventDefault();
    var form = document.querySelector('.ga-form');
    var id = form.id.value;
    if(id === '')
        id = 'UA-XXXX-YY';
    var host = form.host.value;
    if(host === '')
        host = 'your.domain.com';
    var path = form.path.value;
    if(path === '')
        path = '/page/path';
    var link = 'https://notion.doum.app/ga?id=' + id + '&host=' + host + '&path=' + path;
    if(form.hide.checked) {
        link += '&hide=true';
    }
    document.querySelector('#link').textContent = link;
});