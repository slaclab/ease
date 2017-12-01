




class df_controller{
    constructor(prefix, target_fields, replacements, delete_class){
        // take arguments 
        this.prefix = prefix;
        this.target_fields = target_fields;
        this.replacements = replacements;
        this.delete_class = delete_class;

        // inform developer of arg length issue
        if (this.target_fields.length != this.replacements.length){
            throw "target_fields and replacments mush have same length";
        }    
        
        // this.next_contents_no designates the next no. for the next row.
        this.next_contents_no = $('input[name=tg-TOTAL_FORMS]').val();
    }

    add_trigger_actions(){
        // Collection of actions to take when the "add" button is pressed

        var new_contents = $("#contents_section").children().last().clone();

        // Scan through input fields in row, update fields with new names, IDs
        for (var i = 0; i < this.target_fields.length; i++){
            // construct search term to find correct input element
            find = "[id*=id_"+this.prefix+"-][id*=-"+this.target_fields[i]+"]"

            // seek correct input element   
            var target_element = new_contents.find(find)
            
            // construct new ID
            var update_id = "id_"+this.prefix+
                "-"+this.next_contents_no.toString()+
                "-"+this.target_fields[i]
            
            // update correct input element with new ID
            target_element.attr('id', update_id);

            // construct new name
            var update_name = dfc_prefix+
                "-"+this.next_contents_no.toString()+
                "-"+this.target_fields[i]

            // update correct input element with new name
            target_element.attr('name', update_name);            
            
            // update correct imput element with new value 
            new_contents.find(find).val(this.replacements[i]);
        }
    
        // Push new row into live html
        $("#contents_section").append(new_contents);

        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        console.log(cache);
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)+1);

        this.next_contents_no ++;

        new_contents.find(".delete-btn").click(
            //this.delete_trigger_actions.bind(this)
            this.delete_trigger_actions
        );
    
    
    }

    delete_trigger_actions(){
        // reject deleting the last remaining entry, there must be at least one
        // trigger at all times
        if ( $('input[name=tg-TOTAL_FORMS]').val() <= 1 ){
            return;
        }

        $(this).attr('class',"btn btn-danger text-muted")
        //this.innerHTML = "keep this!";
        //$(this).parent().parent().remove();
        $(this).parentsUntil("tbody").last().remove();
        console.log("delete pressed")
        //console.log($(this).parent().parent());
        //console.log($(this).parentsUntil("tbody").last());
        //console.log($(this)[0].innerHTML); 
        
        
        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)-1);
    }

    prepare_document(){
        $("#add_trigger_btn").click(this.add_trigger_actions.bind(this));
        
        $(".delete-btn").click(this.delete_trigger_actions);
    }

};



function dynamic_form_controller(){
    console.log(dfc_prefix);
    console.log(dfc_fields);
    console.log(dfc_replace);



    var next_contents_no = $('input[name=tg-TOTAL_FORMS]').val();


    $("#add_trigger_btn").click(function(){

        if (dfc_fields.length != dfc_replace.length){
            console.log("ARGUMENT LENGTH ERROR");
        }

        var new_contents = $("#contents_section").children().last().clone();

        
        // new_contents.find("input[id*=id_tg-][id*=-new_name]").attr('id','id_tg-'+next_contents_no.toString()+'-new_name');
        // new_contents.find("input[name*=tg-][name*=-new_name]").attr('name','tg-'+next_contents_no.toString()+'-new_name');
        // new_contents.find("input[name*=tg-][name*=-new_name]").val("");

        // new_contents.find("select[id*=id_tg-][id*=-new_pv]").attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").val(-1);








        for (var i = 0; i < dfc_fields.length; i++){
            find = "[id*=id_"+dfc_prefix+
                "-][id*=-"+dfc_fields[i]+"]"
            update = "id_"+dfc_prefix+
                "-"+next_contents_no.toString()+
                "-"+dfc_fields[i]
            new_contents.find(find).attr('id', update);


            find = "[data-id*=id_"+dfc_prefix+
                "-][data-id*=-"+dfc_fields[i]+"]"
            update = "id_"+dfc_prefix+
                "-"+next_contents_no.toString()+
                "-"+dfc_fields[i]
            new_contents.find(find).attr('data-id', update);

            find = "[name*="+dfc_prefix+
                "-][name*=-"+dfc_fields[i]+"]"
            update = dfc_prefix+
                "-"+next_contents_no.toString()+
                "-"+dfc_fields[i]
            new_contents.find(find).attr('name',update);

            find = "[name*="+dfc_prefix+
                "-][name*=-"+dfc_fields[i]+"]"

            new_contents.find(find).val(dfc_replace[i]);
        }

        // new_contents.find("select[id*=id_tg-][id*=-new_pv]").attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents.find("select[name*=tg-][name*=-new_pv]").val(-1);


       
        // new_contents
        //     .find("[id*=id_tg-][id*=-new_name]")
        //         .attr('id','id_tg-'+next_contents_no.toString()+'-new_name');
        // new_contents
        //     .find("[name*=tg-][name*=-new_name]")
        //         .attr('name','tg-'+next_contents_no.toString()+'-new_name');
        // new_contents
        //     .find("[name*=tg-][name*=-new_name]")
        //         .val("");

        // new_contents
        //     .find("[id*=id_tg-][id*=-new_pv]")
        //         .attr('id','id_tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents
        //     .find("[name*=tg-][name*=-new_pv]")
        //         .attr('name','tg-'+next_contents_no.toString()+'-new_pv');
        // new_contents
        //     .find("[name*=tg-][name*=-new_pv]")
        //         .val(-1);




        $("#contents_section").append(new_contents);

        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        console.log(cache);
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)+1);

        next_contents_no ++;
        console.log("click2");


        new_contents.find(".delete-btn").click(delete_handler);


    });



    function delete_handler() {
        if ( $('input[name=tg-TOTAL_FORMS]').val() <= 1 ){
            return;
        }
        //var test = $(this);
        console.log(this);
        console.log($(this));
        $(this).attr('class',"btn btn-danger text-muted")
        //this.innerHTML = "keep this!";
        $(this).parent().parent().remove();
        //console.log($(this)[0].innerHTML); 
        console.log("click_del");
        var cache = $("input[name=tg-TOTAL_FORMS]").val();
        console.log(cache);
        $("input[name=tg-TOTAL_FORMS]").val(Number(cache)-1);
    }


    // handle line deletion

    $(".delete-btn").click(delete_handler);


}
