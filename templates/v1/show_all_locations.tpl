%#template to show all locations
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Sijainnin tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th></tr>
		
	% for l in location_list:
		<tr>
			<th align="left"><a href="/location/show/{{l[0]}}">{{l[0]}}</a></th>
			<th align="left">{{l[1]}}</th>
			<th align="left">{{l[2]}}</th>
			<th align="left"><a href="/location/modify/{{l[0]}}">Muokkaa</a></th>
		</tr>
	% end
</table>
