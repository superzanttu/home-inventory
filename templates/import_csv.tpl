%#template for csv file import
<p>Import database from CSV-file</p>
<form action="/import/" method="POST" enctype="multipart/form-data">
<input type="file" name="csvfile" />
<select name="targettable">
	<option value="">Select target</option>
    <option value="containers">Containers</option>
    <option value="items">Items</option>
    <option value="shelfs">Shelfs</option>
    <option value="annotations">Annotations</option>
    <option value="annotation_lists">Annotation lists</option>
    <option value="item_annotations">Item annotations</option>
</select>
<input type="submit" name="importcsv" value="Import CSV file" />
</form>