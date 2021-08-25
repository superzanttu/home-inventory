%#template for the form for a new item
<form action="/item/add" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Tavaran tunnus</th><th>Vuosi</th><th>Numero</th><th>Nimi</th><th>Laatikko</th></tr>
		<tr>
			<th><input type="text" size="15" value="{{new_item_id}}" readonly name="id"></th>
			<th><input type="number" size="100" value="{{current_year}}" readonly name="year"></th>
			<th><input type="number" size="100" value="{{next_free_item_number}}" readonly name="number"></th>
			<th><input type="text" size="100" name="name"></th>
			<th><select name="box" value="0">
					% for s in box_list:
						% if s[0]=="NoBox":
							<option selected value={{s[0]}}>{{s[0]}}</option>
						% else:
							<option value={{s[0]}}>{{s[0]}}</option>
						% end
					% end
				</select></th>
		</tr>
		<tr>
			<th><input type="submit" name="save" value="Tallenna"></th>
		</tr>
	</table>
</form>