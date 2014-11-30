console.log("ran file")
if(document.getElementById('entity_graph') != null && !/\//.test(document.getElementById("entity_graph").getAttribute("file"))){
console.log('defining functions')

function toggle_hide(hide_action) {
  hide_status = sessionStorage.getItem('graph_hide');
  // sessionStorage.getItem('graph_hide') == 'unhidden'
  console.log(hide_action);
  if(hide_action == 'hide'){
    sessionStorage.setItem('graph_hide','hidden');
    console.log('removing graph tool');
    document.getElementById("entity_graph").innerHTML = "<button type='button' id='hidebutton' onclick=\"toggle_hide('unhide')\">Show graph tool</button>"
  }else{
    sessionStorage.setItem('graph_hide','unhidden');
    setup_graphtool();
  }

  console.log("hide button clicked");
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function draw_graph(gdf, svg, file, width, height) {
  file = file.replace(/_/g, ' ') // we don't use spaces on the filesystem but we want them in our human interface text
  console.log("entity at center: " + file)

  var color = d3.scale.category10();

  var force = d3.layout.force()
      .charge(-300)
      .linkDistance(200)
      .size([width, height]);
  console.log("starting d3")
  d3.json(gdf, function(error, graph) {
    force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();
    console.log("creating links")
    var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });
    console.log("creating nodes")
    var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", function(d){ console.log(d.num_urls); return d.num_urls * 5;}) //hack here
      .style("fill", function(d) { return color(d.group); })
      .style("cursor","move")
      .call(force.drag);
    console.log("creating labels")
    var texts = svg.selectAll("text.label")
      .data(graph.nodes)
      .enter().append("text")
      .attr("class", "label")
      .attr("fill", function(d) {  if (d.name == file) { return "red";} else{ return d.name;}  })
      .on("click", function(d) { window.open(d.url,"_self"); })
      .on("mouseover", function(d){
         if (d.name != file) {
           message = file + " is mentioned on the following page(s) with " + d.name;
           intersection = d.intersection;
           document.getElementById("intersection").innerHTML = message;
           var listElement = document.createElement("ul");
           document.getElementById("intersection").appendChild(listElement);
           for( var i =  0 ; i < intersection.length ; ++i){
             var listItem = document.createElement("li");
             listItem.innerHTML = "<a href='" + intersection[i] + "'>" + intersection[i] + "</a>";
             listElement.appendChild(listItem);
             console.log("tried to add list item");
           }
         }//end of if (d.name != file)
         })
      .style("cursor","pointer")
      .text(function(d) {  return d.name;  });
    console.log("completing configuration")
    node.append("title")
      .text(function(d) { return d.name; });
    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

      texts.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";});
    });
  });

 return
} //end of draw graph function
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function setup_graphtool(){
 document.getElementById("entity_graph").innerHTML = "<div id='graph_container'><b>The graph below shows when <a href='/Category:People'>People</a>, <a href='/Category:Locations'>Places</a>, and <a href='/Category:Organizations'>Organizations</a> are mentioned in articles or web pages together.  <button type='button' id='hidebutton' onclick=\"toggle_hide('hide')\">Hide graph tool</button> \
<hr></b><table><tr><td><div id='graph_vis'></div></td><td><div id='graph_controls'></div></td></tr><tr><td><div id='graph_legend'><img width='350' src='/graph_legend.png'></div></td><td align='right'></td><tr></table></div>";

 document.getElementById("graph_controls").innerHTML = "<p><b>Use this selection to configure the graph. Requiring a higher number of concurrent mentions will result in fewer nodes on the graph which are more strongly correlated to each other.</b></p> \
  Graph links are based on <select id='graph_structure'> \
  <option value='minlinks-1'>being identified on at least 1 external link together</option> \
  <option value='minlinks-2'>being identified on at least 2 external links together</option> \
  <option value='minlinks-3'>being identified on at least 3 external links together</option> \
  <option value='minlinks-4'>being identified on at least 4 external links together</option> \
  <option value='minlinks-5'>being identified on at least 5 external links together</option> \
  <option value='minlinks-6'>being identified on at least 6 external links together</option> \
  </select><br><br><div id='intersection'>...</div>";

 if( sessionStorage.getItem('graph_structure')){
   document.getElementById('graph_structure').value = sessionStorage.getItem('graph_structure');
   console.log("graph_structure set from sessionStorage")
 }else{
   document.getElementById('graph_structure').value = 'minlinks-2'; ////////////////default view
   console.log("graph_structure set to default")
 }

 var e = document.getElementById("graph_structure");
 var graph_structure = e.options[e.selectedIndex].value;
 var file = document.getElementById("entity_graph").getAttribute("file")
 var graph_data_file = "graph_data/" + file + "-" + graph_structure + ".json";

 var width = 800,
    height = 600;

 var svg = d3.select("#graph_vis").append("svg")
  .attr("width", width)
  .attr("height", height);


  draw_graph(graph_data_file, svg, file, width, height);
  console.log("initial graph drawn")

 document.getElementById("graph_structure").onchange = function(){
  console.log("graph structure menu changed")
  var e = document.getElementById("graph_structure");
  var graph_structure = e.options[e.selectedIndex].value;
  var file = document.getElementById("entity_graph").getAttribute("file")
  sessionStorage.setItem('graph_structure',graph_structure);
  graph_data_file = "graph_data/" + file + "-" + graph_structure + ".json";
  d3.selectAll("svg > *").remove(); // removes all elements below svg
  draw_graph(graph_data_file, svg, file, width, height);
  console.log("graph redrawn")
 }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////// nothing but function definitions above here
console.log("Attempting to create graph")
if(sessionStorage.getItem('graph_hide') != 'hidden'){
  toggle_hide('unhide');
}else{
  toggle_hide('hide');
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
} // end of major if statement
