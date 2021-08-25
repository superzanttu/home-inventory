%#template for location modify form
<p>Muokataan sijaintia</p>
<form action="/location/modify/{{location_id}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>Sijainnin tunnus</th>
			<th>Nimi</th>
			<th>Tila</th>
		</tr>
		<tr>
			<th><input type="text" name="id" value="{{location_id}}"></th>
			<th><input type="text" name="name" value="{{location_name}}"></th>
			<th><select name="status" value="0">
					% for s in location_status_list:
						% if s[0]==selected_status_id:
							<option selected value={{s[0]}}>{{s[1]}}</option>
						% else:
							<option value={{s[0]}}>{{s[1]}}</option>
						% end
					% end
				</select></th>
		</tr>
		<tr>
			<th><input type="submit" name="save" value="Tallenna"></th>
		</tr>
  	</table>
</form>