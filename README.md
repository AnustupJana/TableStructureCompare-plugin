# Table Structure Compare QGIS Plugin
![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/icon.png?raw=true)

## Overview
The **Table Structure Compare** plugin for QGIS allows users to compare the attribute table structures of two vector layers. It identifies differences in field names (including case sensitivity), data types, field lengths, field precision, and field order. If the structures are identical, a confirmation popup is displayed. If differences are found, a temporary output layer is created, detailing the discrepancies in a user-friendly table format.

## Features
- Compares two vector layers' attribute table structures.
- Detects the following differences:
  - Case mismatches in field names (e.g., "Other" vs. "OTHER").
  - Type mismatches (e.g., Integer vs. String).
  - Length mismatches (e.g., 80 vs. 100).
  - Precision mismatches (e.g., 3 vs. 10 for Real fields).
  - Order mismatches (fields in different positions).
  - Missing fields in the compare layer.
  - Extra fields in the compare layer.
- Outputs a temporary layer with columns:
  - `B_Field_Name`: Field name from the base layer.
  - `C_Field_Name`: Field name from the compare layer.
  - `Issue`: Semicolon-separated list of issues (e.g., "Case Mismatch; Type Mismatch").
  - `Base_Type`: User-friendly type name from the base layer (e.g., "Integer (64 bit)" instead of "qlonglong").
  - `Compare_Type`: User-friendly type name from the compare layer.
  - `Base_Length`: Field length from the base layer.
  - `Compare_Length`: Field length from the compare layer.
  - `Base_Position`: Field position in the base layer.
  - `Compare_Position`: Field position in the compare layer.
  - `Precision_Issue`: Details of precision mismatches (e.g., "Base: 3, Compare: 10").
- Displays a popup message if the table structures are identical.
- Accessible via the QGIS Processing Toolbox or the plugin's toolbar/menu.

## Installation
1. **From QGIS Plugin Repository**:
   - In QGIS, go to `Plugins > Manage and Install Plugins`.
  
     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/1st.png?raw=true)
   - Search for "Table Structure Compare" in the `All` tab.

     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/2nd.png?raw=true)
   - Click `Install Plugin`.

2. **From ZIP File**:
   - Download the plugin ZIP file from the [GitHub Releases](https://github.com/AnustupJana/TableStructureCompare-plugin.git) page.
   - In QGIS, go to `Plugins > Manage and Install Plugins > Install from ZIP`.
   - Select the downloaded ZIP file and click `Install Plugin`.
  
3. **Download the Plugin**:
   - Clone or download the plugin repository to your local machine.
   - Ensure the folder is named `table_structure_compare`.

4. **From Source (for developers)**:
   - Copy the `table_structure_compare` folder to the QGIS plugins directory:
     - Windows: `C:\Users\[Your Username]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
     - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
     - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
   - Alternatively, use the QGIS Plugin Manager:
     - Go to `Plugins > Manage and Install Plugins`.
     - Select `Install from ZIP` and upload the plugin's ZIP file.

5. **Enable the Plugin**:
   - In QGIS, go to `Plugins > Manage and Install Plugins`.
   - Find `Table Structure Compare` in the `Installed` tab and ensure it is enabled.

6. **Dependencies**:
   - Requires QGIS 3.0 or later.
   - No additional Python packages are required, as it uses QGIS core libraries.

## Usage
1. **Access the Plugin**:
   - Via the **Toolbar**: Click the plugin icon in the QGIS toolbar.
   - Via the **Menu**: Go to `Plugins > Table Structure Compare > Table Structure Compare`.

     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/3rd.png?raw=true)
   - Via the **Processing Toolbox**: Open `Processing > Toolbox`, then find `Vector Analysis > Compare Attribute Table Structure`.

2. **Run the Comparison**:
   - In the Processing Toolbox dialog, select:
     - **Base Vector Layer:** The reference layer.
     - **Compare Vector Layer:** The layer to compare against.
   - Click `Run` to execute the comparison.
  
     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/4th.png?raw=true)

3. **View Results**:
   - If the attribute tables are identical, a message will display:
  
     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/5th.png?raw=true)
   - If differences are found, a temporary layer named "Output Difference Table" will be added to the QGIS project, listing all discrepancies.
  
     ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/6th.png?raw=true)

## Example
Given two layers with the following attribute structures:
- **Base Layer**:
  - Name: String, length 10
  - UUID: Real, length 10, precision 3
  - Number: Integer (64 bit), length 10
  - Alt_Nme: String, length 80
  - Other: String, length 50
  - Field_1: String, length 10
  - Field_2: String, length 10
  - Date: Date, length 10
  - Remark: String, length 50
 
  ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/7th.png?raw=true)
- **Compare Layer**:
  - Name: String, length 10
  - UUID: Real, length 10, precision 10
  - Number: String, length 50
  - Alt_Nme: String, length 100
  - OTHER: String, length 50
  - Field_2: String, length 10
  - Field_1: String, length 10
  - Date: String, length 50
  - Remarks: String, length 50
 
  ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/8th.png?raw=true)

The output table will list differences such as case mismatches (e.g., "Other" vs. "OTHER"), type mismatches (e.g., Integer vs. String), length mismatches, precision mismatches, and order mismatches.

  ![Diagram of the System](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/doc/9th.png?raw=true)

## Development
- **Source Code**: The plugin is written in Python and uses the QGIS Processing framework.
- **Contributing**:
  - Fork the repository and submit pull requests for enhancements or bug fixes.
  - Report issues or feature requests via the repository's [issue](https://github.com/AnustupJana/TableStructureCompare-plugin/issues) tracker.
- **License**: GNU General Public License v2.0 or later. See the [LICENSE](https://github.com/AnustupJana/TableStructureCompare-plugin/blob/main/LICENSE) file for details.

## Contact
- **Name**: Anustup Jana
- **Email**: anustupjana21@gmail.com
- **GitHub**: [Anustup Jana](https://github.com/AnustupJana)

## Notes
- Ensure both input layers are valid vector layers in QGIS.
- The output layer is temporary and can be saved manually if needed.
