

function draw_graph(gdf, svg, file) {
  file = file.replace(/_/g, ' ')
  console.log("entity at center: " + file)

  var color = d3.scale.category10();
  var force = d3.layout.force()
      .charge(-300)
      .linkDistance(200)
      .size([width, height]);


  d3.json(gdf, function(error, graph) {
    force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

    var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", 10)
      .style("fill", function(d) { return color(d.group); })
      .style("cursor","move")
      .call(force.drag);
/*
    var texts = svg.selectAll("text.label")
      .data(graph.nodes)
      .enter().append("text")
      .attr("class", "label")
      .attr("fill", function(d) {  if (d.name == file) { return "red";} else{ return d.name;}  })
      .on("click", function(d) { window.open(d.url,"_self"); })
      .style("cursor","pointer")
      .text(function(d) {  return d.name;  });
*/
    node.append("title")
      .text(function(d) { return d.name; });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

//      texts.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";});
    });
  });


} //end of draw graph function

console.log("ran file")
if(document.getElementById('entity_graph') != null && !/\//.test(document.getElementById("entity_graph").getAttribute("file"))){
console.log("Attempting to create graph")

document.getElementById("entity_graph_menu").innerHTML = "Graph links are based on <select id='graph_structure'> \
  <option value='minlinks-1'>being identified on at least <b>one</b> external link together</option> \
  <option value='minlinks-2'>being identified on at least <b>two</b> external links together</option> \
  <option value='minlinks-3'>being identified on at least <b>three</b> external links together</option> \
  </select>";

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
var svg = d3.select("#entity_graph").append("svg")
  .attr("width", width)
  .attr("height", height);

console.log(graph_data_file)
draw_graph(graph_data_file, svg, file);
console.log("initial graph drawn")

document.getElementById("graph_structure").onchange = function(){
  console.log('option changed');
  var e = document.getElementById("graph_structure");
  var graph_structure = e.options[e.selectedIndex].value;
  console.log(graph_structure)
  sessionStorage.setItem('graph_structure',graph_structure);
  console.log("set sessionStorage graph_structure")
  graph_data_file = "graph_data/" + file + "-" + graph_structure + ".json";
  console.log(graph_data_file)
  d3.selectAll("svg > *").remove(); // removes all elements below svg
  draw_graph(graph_data_file, svg, file);
  console.log("graph redrawn")
}


} // end of if statement
