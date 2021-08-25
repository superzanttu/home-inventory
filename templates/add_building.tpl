% # Add building
<form action="/add/building/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Building ID</th><th>Building Name</th></tr>
		<tr>
			<th><input type="text" size="25"  name="new_building_id"></th>
			<th><input type="text" size="50"  name="new_building_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_building" value="Add new building"></th>
		</tr>
	</table>
</form>