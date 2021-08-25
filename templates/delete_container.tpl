% # Delete container
<form action="/delete/container/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Container</th><th>Confirmation</th></tr>
		<tr>
			<th><select name="selected_container_id" value="0">
					% for s in listContainers:
						<option value={{s[0]}}>{{s[1]}}</option>
					% end
				</select>
			</th>
	
			<th><input type="text" size="25"  name="confirmation_to_delete"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_delete_container" value="Delete container"></th>
		</tr>
	</table>
	<p>Enter container id to approve deletion.</p>
</form>