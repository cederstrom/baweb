$(function() {
	var $body = $('body');
	$body.html($body.html().replace(/\[tm]/g, '&#8482;'));

	$("div[data-toggle=fieldset]").each(function() {
		var $this = $(this);

		$this.find("a[data-toggle=fieldset-add-row]").click(function() {
			var target = $($(this).data("target"));
			console.log(target);
			var nr_of_members = target.find("div[data-toggle=fieldset-entry]").length;
			if(nr_of_members < max_nr_of_members) {
				var oldrow = target.find("div[data-toggle=fieldset-entry]:last");
				var row = oldrow.clone(true, true);
				console.log(row.find(":input")[0]);
				var elem_id = row.find(":input")[0].id;
				var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
				row.attr('data-id', elem_num);
				row.find(":input").each(function() {
					console.log(this);
					var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
					$(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
				});
				row.find("label").each(function() {
					console.log(this);
					var for_id = $(this).attr('for').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
					$(this).attr('for', for_id);
				});
				row.find("div[data-remover]").show();
				oldrow.after(row);
				oldrow.find("div[data-remover]").hide();
			}
			return false;
		});

		$this.find("a[data-toggle=fieldset-remove-row]").click(function() {
			var nr_of_members = $this.find("div[data-toggle=fieldset-entry]").length;
			if(nr_of_members > 1) {
				var thisRow = $(this).closest("div[data-toggle=fieldset-entry]");
				thisRow.remove();
				nr_of_members = nr_of_members - 1;

				if(nr_of_members > 1) {
					var target = $($(this).data("target"));
					var lastrow = target.find("div[data-toggle=fieldset-entry]:last");
					lastrow.find("div[data-remover]").show();
				}
			}
			return false;
		});
	});
});
