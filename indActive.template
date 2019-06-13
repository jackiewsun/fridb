<!DOCTYPE html >
<html>
<head>
  <title>Random Bimetallic Database</title>
  <!--functionality and style scripts-->
  <script src='static/jquery.min.js'></script>
  <script src='static/underscore-min.js'></script>
  <script src='static/bootstrap.min.js'></script>
  <script src='static/sprintf.js'></script>
  <script src='static/clamps.js'></script>
  <script src = "https://rawgit.com/CAYdenberg/Chart.js-ErrorBars/master/dist/Chart.bundle.min.js"></script>
  <div id="multiline"></div>
  <link rel="stylesheet" type="text/css" href="static/bootstrap.min.css"/>
  <link rel="stylesheet" type="text/css" href="static/style.css"/>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body><!--what actually shows up on the webpage-->
  <header id = "main-header">
    <!--<img src = "/home/gce258/Summer_2017_Research/dbstuff/virtual_chem_logo.png" style = "float:left" height="80px">
    <img src = "/home/gce258/Summer_2017_Research/dbstuff/virtual_chem_logo.png" style = "float:right" height="80px">-->
    <h1>The Random Bimetallic Database</h1>
  </header>
  <br>
  <div id = "menu">
    <button id = 'menubtn'> Menu </button>
  </div>
  <div id="dropup">
    <button id="dropbtn">Instructions</button>
    <div id="dropup-content">
      <p>Use the dropdown menu to navigate to the desired combination of the following fields: Structure Type, Binding Site Composition, Adsorbate, and Result Type.</p>
      <p>The 'Graph' option in binding site composition allows simultaneous graphing of binding energies and/or adsorbate movement distances at all binding site compositions for any alloy. Just click on the square corresponding to an alloy/alloys of interest!</p>
    </div>
  </div>
  <br>
  <div class='container btn-group' id='container'>
    <canvas class = "absolute" id="myChart" width="150px" height="100px"></canvas><!--The canvas element for the graph-->
  </div>
  <!--Side Navigation Bar-->
  <div class = 'sidenav' id = 'sidenav'>
    <a href = "javascript:void(0)" class = "closebtn" id = 'closebtn'>&times;</a>
    <a href = '#' id = "home">Home</a>
    <button class = 'dropdown-btn'>79 NP
      <i class = "fa fa-caret-down"></i>
    </button>
    <div class = 'dropdown-container' id = '79_NP'>
    </div>
    <button class = 'dropdown-btn'>Slab
      <i class = "fa fa-caret-down"></i>
    </button>
    <div class = 'dropdown-container' id = 'Slab'>
    </div>
  </div>
  <p class = 'home'>It is essential to promote alternative energy sources as our energy demands to increase. Our research aims to improve the viability of hydrogen
		fuel cells via high-throughput computation of materials candidates for catalysis. We performed density functional theory calculations to optimize randomly-ordered
		bimetallic 79-atom nanoparticles and slabs. We use the well-defined relation between binding energy of metallic materials to oxygen and hydrogen to their catalytic ability
		for the oxygen reduction and hydrogen evolution reactions. From there, we can make conclusions about promising catalytic materials from our calculated binding energies
		reported here.</p>
		<p class = 'home'>Findings reported here also include the distance the adsorbate moved from the original three-fold hollow site, which when considered in the differences
		between predicted and observed binding energies, can explain deviations from our predictions. A useful tool in this database is the 'Graph' functionality, which allows
		plotting of binding energies and/or adsorbate movement distances across the four site compositions for a particular alloy. This can then be used, for example, to observe
		whether one of our materials is tunable and, if not, what sites correlated to adsorbate movement.</p>
</body>
<script>
var ideal_OBE = -1.143;
var ideal_HBE = -0.529;
//Creates dropdown elements for each layer of data e.g. 79NP->AAA/BBB->O->Binding Energy
function makeNewSideDropdown(initial_label, for_dropdowns, i = 0){
  _.each(for_dropdowns[i], function(label) {
    //ensuring no repeat graphs
    if (label == 'ABB' || label == 'BBB') {
      return false;
    }
    //all elements necessary for the HTML
    var new_dropdown_button = document.createElement('button');
    new_dropdown_button.className = 'dropdown-btn';
    var new_dropdown_div = document.createElement('div');
    new_dropdown_div.className = 'dropdown-container';
    new_dropdown_div.id = initial_label.id + '_' + label;
    if (label == 'AAA') {
      label = 'AAA/BBB'
    } else if (label == 'AAB') {
      label = 'AAB/ABB'
    }
    new_dropdown_button.textContent = label;
    var i_element = document.createElement('i');
    i_element.className = 'fa fa-caret-down';
    new_dropdown_button.appendChild(i_element);
    //continues recursively if there are more layers to add to the menu, or else it adds the final layer which has active links
    if((i + 1) < for_dropdowns.length-1) {
      makeNewSideDropdown(new_dropdown_div, for_dropdowns, i+1);
    } else {
      fillInSideDropdown(new_dropdown_div, for_dropdowns[i+1]);
    }
    initial_label.appendChild(new_dropdown_button);
    initial_label.appendChild(new_dropdown_div);
  });
}

//adds the final layer for the side dropdown - has active links that change the active data
function fillInSideDropdown(outer_label, labels){
  _.each(labels, function(result) {
    var a_result = document.createElement('a');
    a_result.textContent = result;
    a_result.href = '#';
    a_result.id = outer_label.id + '_' + result;
    if (a_result.textContent.includes('_')){
      a_result.textContent = a_result.textContent.replace('_', ' ')
    }
    outer_label.appendChild(a_result);
  });
}

//text content of the keys for each input in allresults
function make_keys(A_count, B_count, split) {
  var key = split[0] + '/' + split[1] + '/' + String(A_count) + '/' + split[3] + '/' + String(B_count) + '/' + split[5];
  return key;
};
//here to cut down on some lines of code.
function initialize_tables(tables, tableTitle, tableTitle2, result_type, SiteA, SiteA2) {
  if (!_.has(tables, tableTitle)) {//appends the tables if it isn't already a part of the tables object
    tables[tableTitle] = {max: -1e300, min: 1e300, SiteA: SiteA, result_type:result_type, cells: {'webpage':'colored'}};
    tables[tableTitle2] = {max: -1e300, min: 1e300, SiteA: SiteA2, result_type:result_type, cells: {'webpage':'colored'}};
  }
  return tables;
}
//this function fills in the tables, getting passed a variable that is defined as the container element ID
function fill_tables(contain) {
  var color = [] //empty color array for the purposes of graphing colors
  var SorN = 'Jackie'; //slab or nanoparticle
  var SiteA = 'asdfasdf'; //the two sites, either AAA AAB ABB BBB
  var SiteA2 = 'asdfasdf';
  var dataset1 = []; //empty dataset array for the purpose of graphing (keeping track of which datasets are to be displayed)
  var container = document.getElementById(contain);
  var dblock = ['Ni', 'Pd', 'Rh', 'Pt', 'Ir', 'Cu', 'Au', 'Ag']; //horizontal row of metals
  var dblock2 = [...dblock].reverse(); //vertical row of metals; is the reverse of the horizontal; [...dblock] is used to not alter dblock itself but rather a copy of it
  var data = {{!data}};
  var tables = {}; //new empty object to put all the tables in
  //runs through each set of data. ._each works by going through data as a function of key and value
  _.each(data, function(value, key) {
    //key is like N/Cu/0/Ru/3/O, value is the data in each function
    var split = key.split('/'); //splits the key by element into an array
    var SN = split[0]; //slab or NP
    if (SN == 'S') {
      SorN = 'Slab';
    } else {
      SorN = '79 NP';
    }
    var m1 = split[1]; //first metal
    SiteA = parseInt(split[2]); //# of the first metal. is none if it is a pure slab
    var m2 = split[3]; //second metal
    var SiteB = parseInt(split[4]); //parseInt returns the numerical aspect of the argument. # of the second metal
    var result_type = split[5] + ' Binding Energy'; //O or H binding energy
    var dist = parseFloat(value['distance']); //returns
    var run = parseInt(split[6]); //not a useful line. delete?
    var again = 0;
    if (SiteA === 0) { //designating sites
      SiteA2 = 'AAA';
      SiteA = 'BBB';
    } else if (SiteA === 1) {
      SiteA2 = 'AAB';
      SiteA = 'ABB';
    } else if (SiteA === 2) {
      SiteA2 = 'ABB';
      SiteA = 'AAB';
    } else if (SiteA === 3) {
      SiteA2 = 'BBB';
      SiteA = 'AAA';
    } else { //pure case; just an arbitrary assignment
      SiteA2 = 'BBB';
      SiteA = 'AAA';
    }

    function initialize_table(site, tableTitle_BE, tableTitle_Dist, arg){//value arg is to see if it is title or title2
      if(arg === 0) {
        cellKey = sprintf('%s,%s', m1, m2);
      } else {
        cellKey = sprintf('%s,%s', m2, m1);
      }
      tables[tableTitle_BE]['cells'][cellKey] = {};
      tables[tableTitle_Dist]['cells'][cellKey] = {};
      var val = parseFloat(value['result']);//returns the binding energy
      if (value['deform_RMS'] == null || value['deform_max'] == null) {//
        var deformed = 'deformed';
      } else {
        var deformed = parseFloat(value['deform_RMS']);
      }
      tables[tableTitle_BE]['cells'][cellKey]['actualvalue'] = val;//adding the value into each cell
      tables[tableTitle_Dist]['cells'][cellKey]['actualvalue'] = dist;//distance value for each cell
      if (result_type in clamps) {
        val = Math.max(clamps[result_type]['min'], Math.min(val, clamps[result_type]['max']))
      }
      tables[tableTitle_BE]['cells'][cellKey]['value'] = val;//this entire chunk of code is inserting data into cells
      tables[tableTitle_BE]['cells'][cellKey]['metadata'] = value['metadata'];
      tables[tableTitle_BE]['cells'][cellKey]['username'] = value['username'];
      try {
        tables[tableTitle_BE]['cells'][cellKey]['predicted_BE'] = parseFloat(value['predicted_BE']);
      } catch {
        tables[tableTitle_BE]['cells'][cellKey]['predicted_BE'] = null;
      }
      tables[tableTitle_BE]['cells'][cellKey]['deform'] = deformed;
      tables[tableTitle_Dist]['cells'][cellKey]['metadata'] = 'Distance Moved: ' + String(dist);
      tables[tableTitle_Dist]['cells'][cellKey]['Neighbors'] = parseInt(value['Neighbors']);
      tables[tableTitle_Dist]['cells'][cellKey]['neighbor_identity'] = value['neighbor_identity'];
      tables[tableTitle_Dist]['cells'][cellKey]['deform'] = deformed;
      if (tables[tableTitle_BE]['cells'][cellKey]['username'] == undefined) {//ensuring that you don't have a null username
        tables[tableTitle_BE]['cells'][cellKey]['username'] = "unknown";
      }
      tables[tableTitle_BE]['max'] = Math.max(val, tables[tableTitle_BE]['max']);//identifies the maxes and mins of the table values
      tables[tableTitle_BE]['min'] = Math.min(val, tables[tableTitle_BE]['min']);
      var key0 = make_keys(0, 3, split)//making keys
      var key1 = make_keys(1, 2, split)
      var key2 = make_keys(2, 1, split)
      var key3 = make_keys(3, 0, split)
      var key4 = make_keys('None', 'None', split)
      if ((key0 in data) && (key1 in data) && (key2 in data) && (key3 in data) || (key4 in data)) { //if all the data is present, the graph will be created (ensuring no missing data point)
        tableTitle = sprintf('%s Graph %s', SorN, result_type);//this entire thing is the same as before except it's a graph
        tableTitle_Dist = sprintf('%s Graph %s', SorN, split[5] + ' Distance Moved');//can really be simplified with another function probably
        if (!_.has(tables, tableTitle)) {//if the graph doesn't already exist as an object
          tables[tableTitle] = {//adds a table element for BE
            max: -1e300,
            min: 1e300,
            result_type: result_type,
            cells: {
              'webpage': 'graph'
            }
          };
        }
        if (!_.has(tables, tableTitle_Dist)) {
          tables[tableTitle_Dist] = {//adds a table element for dist.
            max: -1e300,
            min: 1e300,
            result_type: split[5] + ' Distance Moved',
            cells: {
              'webpage': 'graph'
            }
          };
        }
        if (tables[tableTitle]['cells'][cellKey] == undefined) {//if the key doesn't exist, make it a null object so that the table will still be made
          tables[tableTitle]['cells'][cellKey] = {};
        }
        if (tables[tableTitle_Dist]['cells'][cellKey] == undefined) {
          tables[tableTitle_Dist]['cells'][cellKey] = {};
        }
        var val = parseFloat(value['result']);//same thing - adding data to the table
        var std = parseFloat(value['std']);
        var diststd = parseFloat(value['std distance']);
        tables[tableTitle]['cells'][cellKey][site] = {}; //clean up with looping. same thing as before where we're adding data into the graph
        tables[tableTitle_Dist]['cells'][cellKey][site] = {};
        tables[tableTitle]['cells'][cellKey][site]['value'] = val;
        tables[tableTitle]['cells'][cellKey][site]['std'] = std;
        tables[tableTitle_Dist]['cells'][cellKey][site]['distance'] = dist;
        tables[tableTitle_Dist]['cells'][cellKey][site]['std distance'] = diststd;
        if (value['deform_RMS'] == null || value['deform_max'] == null) {
          tables[tableTitle]['cells'][cellKey]['deform'] = 'deformed';
          tables[tableTitle_Dist]['cells'][cellKey]['deform'] = 'deformed';
        }
        if (result_type in clamps) {
          val = Math.max(clamps[result_type]['min'], Math.min(val, clamps[result_type]['max']))
        }
        tables[tableTitle]['cells'][cellKey]['value'] = val;
      }

    }
      tableTitle_BE = sprintf('%s %s %s', SorN, SiteA, result_type); //sprintf is like printf, returning a string based on the values given
      tableTitle2_BE = sprintf('%s %s %s', SorN, SiteA2, result_type) //these ones are simply generating table titles
      tableTitle_Dist = sprintf('%s %s %s', SorN, SiteA, split[5] + ' Distance Moved'); //table is for AAA and BBB
      tableTitle2_Dist = sprintf('%s %s %s', SorN, SiteA2, split[5] + ' Distance Moved'); //table2 is for AAB and ABB
      tables = initialize_tables(tables, tableTitle_BE, tableTitle2_BE, result_type, SiteA, SiteA2);//adds a table object to the group of existing tables
      tables = initialize_tables(tables, tableTitle_Dist, tableTitle2_Dist, split[5] + ' Distance Moved', SiteA, SiteA2);
      initialize_table(SiteA, tableTitle_BE, tableTitle_Dist, 0);//BBB
      initialize_table(SiteA2, tableTitle2_BE, tableTitle2_Dist, 1);//AAA
      if (key.includes('None')) {
        SiteA2 = 'ABB';
        SiteA = 'AAB';
        tableTitle_BE = sprintf('%s %s %s', SorN, SiteA, result_type); //sprintf is like printf, returning a string based on the values given
        tableTitle2_BE = sprintf('%s %s %s', SorN, SiteA2, result_type) //these ones are simply generating table titles
        tableTitle_Dist = sprintf('%s %s %s', SorN, SiteA, split[5] + ' Distance Moved'); //table is for AAA and BBB
        tableTitle2_Dist = sprintf('%s %s %s', SorN, SiteA2, split[5] + ' Distance Moved'); //table2 is for AAB and ABB
        tables = initialize_tables(tables, tableTitle_BE, tableTitle2_BE, result_type, SiteA, SiteA2);//adds a table object to the group of existing tables
        tables = initialize_tables(tables, tableTitle_Dist, tableTitle2_Dist, split[5] + ' Distance Moved', SiteA, SiteA2);
        initialize_table(SiteA, tableTitle_BE, tableTitle_Dist, 0);//AAB
        initialize_table(SiteA2, tableTitle2_BE, tableTitle2_Dist, 1);//ABB
      }
  });
  return [color, dataset1, container, dblock, dblock2, tables];//the result of fill_tables is an array
}

function make_table(contain) {
  needed_vars = fill_tables(contain); //calls the function fill_tables to gather the necessary data
  var color = {},//empty color object
    container = needed_vars[2],//container HTML object
    dblock = needed_vars[3],//metals for horizontal
    dblock2 = needed_vars[4],//metals for vertical
    tables = needed_vars[5];//the table objects
  dataset1 = [
    {label: 'Ideal OBE', fill: false, data: [ideal_OBE, ideal_OBE, ideal_OBE, ideal_OBE], type: 'lineError', yAxisID: 'BE'},
    {label: 'Ideal HBE', fill: false, data: [ideal_HBE, ideal_HBE, ideal_HBE, ideal_HBE], type: 'lineError', yAxisID: 'BE'},
    {data: [0,0,0,0], yAxisID: 'Dist'}
  ]; //initial dataset for the graph - 0 line to fix positioning, other 2 for ideal energies
  var ids = ["79_NP", "Slab"];//helps with generating the dropdowns
  var siteAs = ['AAA', 'AAB', 'ABB', 'BBB', 'Graph'];
  var adsorbate = ["O", "H"];
  var result_type = ["Binding_Energy", "Distance_Moved"];
  var for_dropdowns = [siteAs, adsorbate, result_type];
  _.each(ids, function(label) {//loop to create dropdowns
    var structure = document.getElementById(label);
    makeNewSideDropdown(structure, for_dropdowns);
  });

  var nuke = document.createElement('button'); //makes clear button
  nuke.textContent = "clear";
  nuke.className = "btn btn-default";
  container.appendChild(nuke);

  var OBE = document.createElement('button');//ideal OBE
  OBE.textContent = "ideal OBE";
  OBE.className = "btn btn-default";
  container.appendChild(OBE);

  var HBE = document.createElement('button');//ideal OBE
  HBE.textContent = "ideal HBE";
  HBE.className = "btn btn-default";
  container.appendChild(HBE);

  tableContainers = {};
  var ctx = document.getElementById("myChart").getContext('2d');
  var config = { //clean up using CSS //all of these are settings for the graph (60+lines)
    type: 'bar',
    data: {
      labels: ["AAA", "AAB", "ABB", "BBB"],
      datasets: dataset1
    },
    options: {
      responsive: true,
      legend: {
        display: true,
        position: "bottom",
        fontSize: 16
      },
      scales: {
        xAxes: [{
          stacked: false, //false to put bars adjacent
          type: 'category',
          display: true,
          barThickness: 33,
          ticks: {
            fontSize: 16
          },
          position: 'bottom',
          scaleLabel: {
            display: true,
            labelString: 'Binding Site',
            fontSize: 25
          }
        }, {
          stacked: false,
          type: 'category',
          display: false,
          position: 'bottom'
        }],
        yAxes: [{
          id: 'BE',
          type: 'linear',
          display: true,
          ticks: {
            fontSize: 16
          },
          scaleLabel: {
            id: 'BE',
            display: true,
            labelString: 'Binding Energy (eV)',
            fontSize: 25
          }
        }, {
          id: 'Dist',
          stacked: false,
          type: 'linear',
          position: 'right',
          display: true,
          gridLines: {
            display: false
          },
          ticks: {
            fontSize: 16
          },
          scaleLabel: {
            id: 'Dist',
            display: true,
            labelString: 'Distance Moved (Angstroms)',
            fontSize: 25
          }
        }]
      }
    }
  };
  Chart.defaults.global.defaultFontColor = "black"; //fontcolor, changes all
  window.onload = function() {//when the page loads, create this chart object in the canvas
    window.myLine = new Chart(ctx, config);
    dataset1.splice(2,1);//remove the 0 bar that was just there to fix spacing
    window.myLine.update();
  }
  _.each(tables, function(table, title) { //loops through each table in tables, utilizing their contents and title
    var tableContainer = document.createElement('div');
    var titleSplit = title.split(' ').join('_');
    var OorH = "O";//determines which type of graph it is
    if (titleSplit.split('_').indexOf("H") > -1) {
      OorH = "H";
    }
    if (titleSplit.split('_').indexOf("Graph") > -1) {
      OorH = "Graph";
    }
    tableContainers[titleSplit] = tableContainer; //creates HTML element for table
    tableContainer.id = titleSplit; //gives element unique id for differentiation
    container.appendChild(tableContainer); //puts table into document container
    var heading = document.createElement('h3');//heading element (h# is importance)
    tableContainer.appendChild(heading);
    if (title.includes('AAA')) {//proper title construction
      title = title.replace('AAA', 'AAA/BBB');
    } else if (title.includes('AAB')) {
      title = title.replace('AAB', 'AAB/ABB');
    }
    titleChange = title;
    if (OorH == "O") {
      titleChange = title.replace('Binding Energy', 'Activity');
    }
    heading.textContent = titleChange;
    heading.style.fontSize = "xx-large"
    var tableElement = document.createElement('table');
    tableContainer.appendChild(tableElement);
    var coreLabelled = false;//is the core (Metal B) created?
    var keyLabelled = false;//is the key (color gradient) created?
    _.each(dblock2, function(m2) {//for each m2 in the vertical
      var tr = document.createElement('tr');//adds a row
      tableElement.appendChild(tr);
      if (!coreLabelled) {//labels the core if it isn't already labeled
        var td = document.createElement('td');
        td.rowSpan = dblock2.length + 1;
        td.style.border = "none";
        tr.appendChild(td);
        var label = document.createElement('div');
        label.innerHTML = '<h3 id="core-label">Metal B</h3>';
        td.appendChild(label);
        coreLabelled = true;
      }
      var td = document.createElement('td');//create a table cell for the label
      td.textContent = m2; //labels with a B metal
      td.style.fontSize = "large";
      //td.style.fontFamily = 'lucida console'
      tr.appendChild(td);//adds a cell
      td.style.width = "50px";//styling
      tr.style.height = '50px';
      _.each(dblock, function(m1) {//for each m1 in the horizontal
        var td = document.createElement('td');//create a cell for the data
        cellKey = sprintf('%s,%s', m1, m2);//names the cell for the proper data
        if (_.has(table['cells'], cellKey)) {//if the cell's data exists, add data
          var diff = table['max'] - table['min'];
          diff = Math.max(1, diff); // prevent divide by zero when max == min.
          var val = table['cells'][cellKey]['value'];
          if (table['cells'][cellKey]['deform'] == 'deformed') {
            td.style.background = sprintf('#000000')
            //												td.style.fontSize = "large"
            //												td.textContent = 'X'
          } else if (table['result_type'] == "O Binding Energy") { //creates color gradient for O
            var target_energy = ideal_OBE;
              var ideal_activity = -0.134;
              if(val < target_energy) { //overbinding
                var activity = 0.7642240985316116 + 0.7854675573688066 * val
                table['cells'][cellKey]['value'] = activity
                var activityRatio = activity / (-2)
                td.style.background = sprintf('rgb(0,' + String(91 + Math.min(Math.floor(activityRatio * (247 - 91)), 247 - 91)) + ',0)')
              } else { //underbinding
                var activity = -3.001067465601418 - 2.507767421216152 * val
                table['cells'][cellKey]['value'] = activity
                var activityRatio = activity / (-2)
                td.style.background = sprintf('rgb(255,' + String(57 + Math.min(Math.floor(activityRatio * (183 - 57)), 183 - 57)) + ',0)')
              }
              /*//binding energy
              var dif = Math.abs(target_energy - val);
              if (dif < 0.1) {
                td.style.background = sprintf('#AD0000') //all are shades of red
              } else if (dif < 0.3) {
                td.style.background = sprintf('#FF0000') //color gradient make it a function
              } else if (dif < 0.5) {
                td.style.background = sprintf('#FF2424')
              } else if (dif < 0.7) {
              td.style.background = sprintf('#FF3535')
              } else if (dif < 0.9) {
                td.style.background = sprintf('#FF474F')
              } else if (dif < 1.1) {
                td.style.background = sprintf('#FF6B6B')
              } else if (dif < 1.3) {
                td.style.background = sprintf('#FF7D7D')
              } else if (dif < 1.5) {
                td.style.background = sprintf('#FF8F8F')
              } else {
                td.style.background = sprintf('#FFC4C4')
              }*/
          } else if (table['result_type'] == "H Binding Energy") { //creates color gradient for H
            var target_energy = ideal_HBE;
            var dif = Math.abs(target_energy - val);
            if (dif < 0.05) {
              td.style.background = sprintf('#0036B0') //all are shades of blue
            } else if (dif < 0.1) {
              td.style.background = sprintf('#2B58BD')
            } else if (dif < 0.15) {
              td.style.background = sprintf('#4068C4')
            } else if (dif < 0.2) {
              td.style.background = sprintf('#5579CA')
            } else if (dif < 0.3) {
              td.style.background = sprintf('#6A8AD1')
            } else if (dif < 0.4) {
              td.style.background = sprintf('#809BD7')
            } else if (dif < 0.5) {
              td.style.background = sprintf('#95ABDE')
            } else if (dif < 0.6) {
              td.style.background = sprintf('#AABCE5')
            } else {
              td.style.background = sprintf('#BFCDEB')
            }
          } else if (table['result_type'].includes("Distance")) { //creates color gradient for H
            var dist = table['cells'][cellKey]['actualvalue']
            var ratioHollow = dist / (0.4)//creates values to use for determing the binding energy color gradient
            var ratioBridge = dist / (1 - 0.4)
            var ratioTop = dist / (1.5 - 1)
            var neighbors = table['cells'][cellKey]['Neighbors'];

            if (neighbors == 1) {//creating the color gradient based on which site the adsorbate is binded to
              td.style.background = sprintf('rgb(0,' + String(91 + Math.min(Math.floor(ratioTop * (247 - 91)), 247 - 91)) + ',0)')
            } else if (neighbors == 2) {
              td.style.background = sprintf('rgb(99,50,' + String(83 + Math.min(Math.floor(ratioBridge * (208 - 83), 208 - 83))) + ')') //why the numbers??
            } else if (neighbors == 3) {
              td.style.background = sprintf('rgb(255,' + String(57 + Math.min(Math.floor(ratioHollow * (183 - 57)), 183 - 57)) + ',0)')
            }
          }
          if (table['cells']['webpage'] == 'colored') {//if the data exists, create data
            div = document.createElement('div');
            div.title = sprintf('Alloy: %s%s\n', m1, m2)
            var onSite = [];
            if (title.includes('AAA')) {//checking to make sure that you're adding data to the right table
              if (dblock[m1] < dblock[m2]) {
                onsite = [m2, m2, m2];
              } else {
                onSite = [m1, m1, m1];
              }
            } else if (title.includes('AAB')) {
              if (dblock[m1] < dblock[m2]) {
                onSite = [m1, m2, m2];
              } else {
                onSite = [m1, m1, m2];
              }
            }
            div.title += 'On Site: ' + onSite.join('') + '\n'
            //noting (if changed sites) where the site change is
            if(titleSplit.split('_').indexOf("Distance") > -1){
              var neighbor_identities = table['cells'][cellKey]['neighbor_identity'];
              var neighbor_identities_array = {};
              _.each(neighbor_identities, function(site){
                var siteKey = site.sort().join('');
                try {
                  neighbor_identities_array[siteKey][0]++;
                } catch {
                  neighbor_identities_array[siteKey] = [1, siteKey];
                }
              }); //issue is finding the site name vs cellKey
              delete neighbor_identities_array[onSite.sort().join('')];
              _.each(neighbor_identities_array, function(siteKey){
                div.title += sprintf('Moved to Site %s %s times\n', siteKey[1], siteKey[0])
              })
            }
            if (table['cells'][cellKey]['deform'] == 'deformed') {//if deformed, add data to the tooltip
              div.title += sprintf('Significantly deformed upon adsorption.')
            } else {//if it isn't deformed, add the data to the tooltip
              if (titleSplit.split('_').indexOf("Distance") == -1) {
                div.title += 'Activity: ' + table['cells'][cellKey]['value'].toFixed(4) + '\n';
                div.title += 'Predicted Binding Energy: ' + table['cells'][cellKey]['predicted_BE'] + '\n';
              }
              div.title += table['cells'][cellKey]['metadata'].replace(/<br>/g, '\n');
            }
            div.style.width = '100%';
            div.style.height = '100%';
            div.style.opacity = "1";
            $(div).tooltip();//makes the popup part of the datasets
            td.appendChild(div);
          } else {
            if (table['cells'][cellKey]['deform'] == 'deformed') {//makes the deformed ones black
              td.style.background = sprintf('#000000')
            } else {//creates a clickable button to create a graph
              hope = document.createElement('button');
              td.style.background = sprintf('rgb(230,230,210)');
              td.className = "clickfalse"; //indicates if the button is toggled or not
              var ret = title.replace(' Graph', '')
              hope.style.width = '50px';
              hope.style.height = '50px';
              hope.style.opacity = "0.0";

              function add() { //add dataset to dataset1
                cellKey = sprintf('%s,%s', m1, m2);
                var in_color = false;
                var hue = 'rgb(' + (Math.floor(Math.random() * 200)) + ',' + (Math.floor(Math.random() * 200)) + ',' + (Math.floor(Math.random() * 200)) + ')';//random color
                var leng = dataset1.length//ensures it is appended at end of dataset1
                var key = cellKey + title.replace(table['result_type'], '')
                for (var entry in color) {
                  if (entry.includes(key)) { // if same alloy in same order, uses same color for plotting line & bar
                    hue = color[entry];//if the alloy already exists, set the color to be what it is for line/bar
                    in_color = true;//exists!
                    break;
                  }
                };
                var keepBorder = hue;
                if (table['result_type'].includes('Distance')) {
                  hue = hue.replace(')', ',0.5)') // makes bars transparent
                  hue = hue.replace('rgb', 'rgba')
                }
                if (hue.includes('rgbaa')) {//fix a small error
                  hue = hue.replace('rgbaa', 'rgba')
                  hue = hue.replace(',0.5)', ')')
                }
                if (!in_color) {//if it doesn't exist already in the dataset, add it
                  color[key + String(leng)] = hue;
                } else {//if it does exist, adjust it to be the same as before
                  if (hue.includes('rgba') && table['result_type'].includes('Binding')) {
                    hue = hue.replace(',0.5)', ')'); // makes bars transparent
                    hue = hue.replace('rgba', 'rgb');
                    keepBorder = hue;
                  }
                  color[key + String(leng)] = hue;
                }
                td.style.background = sprintf(hue);
                if (table['result_type'].includes('Binding')) {//determining if it's line or bar graph
                  var graphType = 'lineError'
                  var axisID = 'BE'
                  var error = 'std'
                  var errorCapWidth = 2.0
                } else {
                  var graphType = 'barError'
                  var axisID = 'Dist'
                  var error = 'std distance'
                  var errorCapWidth = 0.25
                }

                function get_dataset1(result) {//add data to the graph dataset when you click on the button
                  dataset1[leng] = { //info
                    label: (cellKey + " " + ret),
                    fill: false,
                    backgroundColor: hue, // for bars
                    borderWidth: 2, // for bars
                    borderColor: keepBorder, //for bars and lines
                    pointBackgroundColor: color[key + leng],
                    pointBorderColor: color[key + leng],
                    pointHoverBackgroundColor: color[key + leng],
                    pointHoverBorderColor: color[key + leng],
                    errorColor: keepBorder,
                    errorCapWidth: errorCapWidth,
                    data: [
                      table['cells'][cellKey]['AAA'][result],
                      table['cells'][cellKey]['AAB'][result],
                      table['cells'][cellKey]['ABB'][result],
                      table['cells'][cellKey]['BBB'][result]
                    ],
                    error: [
                      table['cells'][cellKey]['AAA'][error] / 2,
                      table['cells'][cellKey]['AAB'][error] / 2,
                      table['cells'][cellKey]['ABB'][error] / 2,
                      table['cells'][cellKey]['BBB'][error] / 2
                    ],
                    tension: 0, //no curving of connecting lines
                    type: graphType,
                    yAxisID: axisID
                  };
                }
                if (table['result_type'].includes('Binding')) {//making sure to get the right dataset
                  get_dataset1('value')
                } else if (table['result_type'].includes('Distance')) {
                  get_dataset1('distance')
                }
              }
              hope.onclick = function() { //adds data to the graph every time a cell is clicked
                cellKey = sprintf('%s,%s', m1, m2);
                var key = cellKey + title.replace(table['result_type'], '')
                var len = dataset1.length;
                var location = -1; //-1 indicates not in dataset1
                for (var i = 0; i < len; i++) { //searches dataset1 to see if it already exists
                  if (dataset1[i]['label'] == (cellKey + " " + ret)) {
                    location = i;
                    break;
                  }
                }
                if (location == -1) { //adds if not in dataset1
                  add();
                } else {
                  dataset1.splice(location,1); //splice cuts out the data from the dataset
                  delete color[key + String(dataset1.length)]
                  td.style.background = sprintf('rgb(230,230,210)');
                }
                window.myLine.update(); //remove line from graph
                if (td.className == "clickfalse") {
                  td.className = "clicktrue" //active = true;
                } else {
                  td.className = "clickfalse"; //active = false;
                }
              }
              $(hope).tooltip();
              td.appendChild(hope);
            }
          }
        }
        tr.appendChild(td);
        td.style.width = '50px';
      });
      if (!keyLabelled && OorH != "Graph") { //adds gradient bars
        function makeGradient(start_color, stop_color, x_coord, grd_label_start, grd_label_stop) {
          var td = document.createElement('td');//new cell for the gradient
          td.rowSpan = dblock.length + 1;
          td.style.border = "none";
          td.width = "100px"
          tr.appendChild(td);
          var gradient = document.createElement('canvas');//canvas is a graphics element
          gradient.id = "gradient" + titleSplit + String(x_coord);
          gradient.height = 250;
          gradient.width = 50;
          td.append(gradient);
          var c = document.getElementById("gradient" + titleSplit + String(x_coord))
          var ctx = c.getContext("2d");
          var grd = ctx.createLinearGradient(x_coord, 20, x_coord, 205)
          ctx.font = "10px Verdana"
          grd.addColorStop(0, start_color)
          grd.addColorStop(1, stop_color)
          ctx.fillText(grd_label_start, 0, 10)
          ctx.fillText(grd_label_stop, 0, 240)
          ctx.fillStyle = grd;
          ctx.fillRect(0, 20, c.width, 205);
          keyLabelled = true;
        }
        if (title.includes("Distance")) {//making the various gradients for different tables
          makeGradient("#005B00", "#00F700", 0, "Top <1.0 Ang", " >1.5 Ang")
          makeGradient("#633253", "#6332D0", 10, "Bridge <0.4 Ang", " >1.0 Ang")
          makeGradient("#FF3900", "#FFB700", 20, "Hollow <0.05 Ang", " >0.4 Ang")
        } else if (OorH == "O") {
          makeGradient("#005B00", "#00F700", 0, "Over,ideal", "Non-ideal")
          makeGradient("#FF3900", "#FFB700", 10, "Under,ideal", "Non-ideal")
        } else if (OorH == "H") {
          makeGradient("#0036B0", "#BFCDEB", 0, "<0.05 eV", " >0.6 eV")
        }
      }
    });
    var tr = document.createElement('tr');
    tableElement.appendChild(tr);
    var td = document.createElement('td');
    tr.appendChild(td);
    tr.style.height = '50px';
    _.each(dblock, function(m1) {
      var td = document.createElement('td');
      td.textContent = m1; //Labels the a metals
      td.style.fontSize = "large";
      //td.style.fontFamily = 'lucida console'
      tr.appendChild(td);
    });
    var tr = document.createElement('tr');//buffer space so that the labels don't all get meshed together
    tableElement.appendChild(tr);
    var td = document.createElement('td');
    tr.appendChild(td);
    td.style.border = "none";
    var td = document.createElement('td');
    tr.appendChild(td);
    td.innerHTML = '<h3>Metal A</h3>';
    td.setAttribute('colspan', dblock.length + 1);
    td.style.border = 'none';
  });

  function hideAllTables() {//all tables are hidden on the page so we can select which to choose at any point
    _.each(tableContainers, function(div) {
      div.style.display = 'none';
    });
  }
  hideAllTables();
  $(".container").hide();

  function showTable(title) {//for a chosen table, display to the page
    tableContainers[title].style.display = "block";
  }

  jQuery(".sidenav a").click(function() {
    //functionality of dropdown menu
    var contentPanelId = jQuery(this).attr("id");//grab id of the table chosen via dropdown menu
    if (contentPanelId == "home") {
      hideAllTables();
      $(".container").hide();
      //$(".btn btn-default").hide();
      $(".home").show();
    }
    else if (contentPanelId != 'closebtn' && contentPanelId != undefined) {//otherwise, hide away whatever is on the page now and display the chosen table
      hideAllTables();
      showTable(contentPanelId);
      $(".container").show();
      //$(".btn btn-default").show();
      $(".home").hide();
    }
  });

  nuke.onclick = function() { //clear button functionality
    var BE = 0;
    //so that the ideal BE lines don't disappear when the graph is cleared
    try{
      for(i = 0; i < 2; i++){
        if(dataset1[i]['label'] == 'Ideal HBE' || dataset1[i]['label'] == 'Ideal OBE'){
          BE += 1;
        }
      }
    } catch {} //if the dataset is empty AKA no lines on the graph
    dataset1.splice(BE, dataset1.length); //remove all data currently on the graph
    color = {};//empty out color record
    window.myLine.update();//have graph reflect the above changes
    var allGray = document.getElementsByClassName('clicktrue'); //gets all table elements and clears
    var leng = allGray.length;
    for (var i = 0; i < leng; i++) {
      allGray[0].style.background = sprintf('rgb(230,230,210)'); //is set to 0 because allGray is dynamically changing everytime you change the classname
      allGray[0].className = "clickfalse";
    }
  }

  OBE.onclick = function() {//adding and removing the OBE line
    try {
      if(dataset1[0]['label'] != 'Ideal OBE') {
        dataset1.splice(0, 0, {label: 'Ideal OBE', fill: false, data: [ideal_OBE, ideal_OBE, ideal_OBE, ideal_OBE], type: 'lineError', yAxisID: 'BE'});
      }
      else {
        dataset1.splice(0, 1);
      }
    } catch {
      dataset1.splice(0, 0, {label: 'Ideal OBE', fill: false, data: [ideal_OBE, ideal_OBE, ideal_OBE, ideal_OBE], type: 'lineError', yAxisID: 'BE'});
    }
    window.myLine.update();
  }

  HBE.onclick = function() {//adding and removing the Ideal HBE line
    var caught = 0;
    try {//used to catch errors
      var pos;
      //the error is that there may not be 2 elements in the array to check
      if(dataset1[0]['label'] == 'Ideal HBE'){
        pos = 0;
      }
      else if(dataset1[0]['label'] == 'Ideal OBE'){
        caught = 1;
        pos = 1;
      }
      if(dataset1[pos]['label'] != 'Ideal HBE') {
        dataset1.splice(1, 0, {label: 'Ideal HBE', fill: false, data: [ideal_HBE, ideal_HBE, ideal_HBE, ideal_HBE], type: 'lineError', yAxisID: 'BE'});
      }
      else {
        dataset1.splice(pos, 1);
      }
    } catch {//if dataset1 is empty
      dataset1.splice(caught, 0, {label: 'Ideal HBE', fill: false, data: [ideal_HBE, ideal_HBE, ideal_HBE, ideal_HBE], type: 'lineError', yAxisID: 'BE'});
    }
    window.myLine.update();
  }

  //creates expand/collapse functionality for the side navigation bar
  var dropdown = document.getElementsByClassName("dropdown-btn");
  for (var i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var dropdownContent = this.nextElementSibling;
      if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
      } else {
        dropdownContent.style.display = "block";
      }
    });
  }

  document.getElementById('menubtn').addEventListener('click',  function() {
      document.getElementById("sidenav").style.width = "250px";
  });
  document.getElementById('closebtn').addEventListener('click', function () {
      document.getElementById("sidenav").style.width = "0";
  });

}
make_table('container') //'container' id is of the HTML element container
</script>

</html>
