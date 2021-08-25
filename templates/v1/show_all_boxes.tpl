%#template to show all boxes
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Laatikon tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Sijainti</th>
		<th align="left">Täyttöaste</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th></tr>
	% for b in box_list:
		<tr>
			<th align="left"><a href="/box/show/{{b[0]}}">{{b[0]}}</a></th>
			<th align="left">{{b[1]}}</th>
			<th align="left"><a href="/location/show/{{b[2]}}">{{b[2]}}</a></th>
			<th align="left">{{b[3]}} %</th>
			<th align="left">{{b[4]}}</th>
			<th align="left"><a href="/box/modify/{{b[0]}}">Muokkaa</a></th></tr>
	% end
</table>
