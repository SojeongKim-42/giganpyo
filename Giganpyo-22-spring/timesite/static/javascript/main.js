var flag = 0;

function viewDisplay(a) {
    var dis = document.getElementById("clickToView-" + a);
    if (dis.style.display == 'none') {

        dis.style.display = 'block';
    } else {

        dis.style.display = 'none';
    }
}

function viewDisplay2() {
    var dis = document.getElementById("clickToView");
    if (dis.style.visibility == 'hidden') {
        dis.style.visibility = 'visible';
    } else {
        dis.style.visibility = 'hidden';
    }
}

function viewDisplay3(a) {
    var dis = document.getElementById("view-" + a);
    if (dis.style.display == 'none') {
        if (flag == 0) {
            var dis = document.getElementById("view-" + a);
            flag = a;
            dis.style.display = 'block';
        } else {
            var dis = document.getElementById("view-" + flag);
            dis.style.display = 'none';
            var dis = document.getElementById("view-" + a);
            flag = a;
            dis.style.display = 'block';

        }

    } else {
        dis.style.display = 'none';
    }
}

function viewDisplay4() {
    var dis = document.getElementById("clickToView2");
    if (dis.style.display == 'none') {
        dis.style.display = 'block';
    } else {
        dis.style.display = 'none';
    }
}