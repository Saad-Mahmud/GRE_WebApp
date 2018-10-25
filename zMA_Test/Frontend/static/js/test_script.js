var answer = '';

    function check(ans) {
        document.getElementById("clicked").innerHTML = 'You have clicked ' + ans;
        answer = ans;
    }


    function nextTestWord(source, sessionID) {
        console.log('abccccccccc', answer);
        document.getElementById("clicked").innerHTML = ' ';

        var exampleForm = document.forms['mara'];
        for( var i=0; i<exampleForm.length; i++ ){
            if( exampleForm[i].type  === 'radio' && exampleForm[i].checked == true )
            {
                exampleForm[i].checked = false;
            }
        }

        $.ajax({
            url: '/nexttestword',
            data: {'answer': answer, 'sessionID': sessionID, 'buttonID': source.id},
            dataType: 'json',
            type: 'POST',
            success: function (response) {
                console.log(response.option_dict[0][0]);
                document.getElementById("line").innerHTML = response.test_line;

                var $label = $('input[id=radio_btn1]').next();
                $label.text(response.option_dict[0][0]);
                $("#radio_btn1").val(response.option_dict[0][0]);
                $label = $('input[id=radio_btn2]').next();
                $label.text(response.option_dict[1][0]);
                $("#radio_btn2").val(response.option_dict[1][0]);
                $label = $('input[id=radio_btn3]').next();
                $label.text(response.option_dict[2][0]);
                $("#radio_btn3").val(response.option_dict[2][0]);
                $label = $('input[id=radio_btn4]').next();
                $label.text(response.option_dict[3][0]);
                $("#radio_btn4").val(response.option_dict[3][0]);
            },
            error: function (error) {
                console.log('bal');
            }
        });
    }