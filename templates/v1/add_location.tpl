%#template for the form for a new location
<form action="/location/add" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Sijainnin tunnus</th><th>Nimi</th></tr>
		<tr>
			<th><input type="text" name="id"></th>
			<th><input type="text" name="name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="save" value="Tallenna"></th>
		</tr>
  	</table>
</form>