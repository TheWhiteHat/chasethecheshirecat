function toggleShowSubmit()
{ 
    var elems = document.getElementsByTagName('*'), i;
    console.log(elems.length);
    for (i in elems)
    {
        if((" " + elems[i].className + " ").indexOf(" hidden ") > -1)
        {
            console.log('going thru and id is ');
            if (document.getElementById('showSubmitted').checked == true){
                elems[i].style.display = 'none';
            }
            else{
                elems[i].style.display = 'block';
            }
        }
    }
}