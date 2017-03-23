$(function() {
	$("div[data-toggle=fieldset]").each(function() {
		var $this = $(this);

		$this.find("a[data-toggle=fieldset-add-row]").click(function() {
			var my_non_sfs_count = $( "input:checkbox:checked[id*='sfs']" ).length;
			$.ajax({
				url: "/flumride/number_of_non_sfs_left",
				async: false,
				success: function(data) {
					console.log(data.number_of_non_sfs_left + " - " + my_non_sfs_count);
					block_non_sfs = ((data.number_of_non_sfs_left - my_non_sfs_count) <= 0);
				}
			});

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
					$(this).attr('name', id).attr('id', id).removeAttr("checked");
					if (block_non_sfs && id.indexOf('sfs') !== -1) {
						$(this).prop("checked", true);
						$(this).prop("readonly", true);
						$(this).attr('onclick', '').click(function() {
							alert(message_no_non_sfs_left);
							return false;
						});
					}
					if($(this).is(':checkbox') === false) {
						$(this).val('');
					}
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

		$this.find("input[name$=-person_number]").blur(function() {
		    var value = $(this).val();
		    value = value.replace(" ", "");

            var length = value.length;
		    if (length >= 10 && length <= 13) {
		        if (value.indexOf("-") === -1) {
		            value = value.slice(0, length - 4) + "-" + value.slice(length - 4);
		        }
		    }

		    $(this).val(value);
		});
	});
});
