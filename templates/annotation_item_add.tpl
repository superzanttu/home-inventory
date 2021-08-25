% # Add annotation
<form action="/annotation/add/{{editItemID}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>Add</th>
			<th>Text</th>
			<th>Value</th>
		</tr>
		% for a in listAnnotations:
			<tr>
				<th><input type="checkbox" name="annotation_selected" value="{{a[0]}}"></th>
				<th>{{a[3]}}</th>
				<th>
					% if a[1]=="LIST":	
						<select name="annotation_value_{{a[0]}}">
							<option value="">Not selected</option>
							% for i in listAnnotationListItems:
								% if i[0] == a[2]:
									<option value="{{i[1]}}">{{i[1]}}</option>
								% end
							% end
						</select>
					% elif a[1]=="DATE":
						<input name="annotation_value_{{a[0]}}" type="date" min="2017-01-01" max="2050-01-01">
					% elif a[1]=="TEXT":
						<input type="text" size="25"  name="annotation_value_{{a[0]}}">
					% else:
						Unknown type!
					{{a[1]}}
					% end
				</th>			
			</tr>
		% end
		<tr>
			<th>
				<input type="submit" name="button_annotation_add_save" value="Save">
				<input type="reset" name="button_annotation_add_cancel" value="Reset">
			</th>
		</tr>
	</table>

