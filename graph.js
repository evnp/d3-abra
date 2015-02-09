var width = $('body').width(),
    height = $('body').height();

var color = d3.scale.category10();
// var color = d3.scale.ordinal()
//     .domain(_.range(1, 11))
//     .range(_.filter(d3.scale.category10().range(), function (color, i) {
//         return i % 2 === 0;
//     }));

var force = d3.layout.force()
    .charge(-3000)
    .friction(0.5)
    .linkStrength(0.8)
    .linkDistance(200)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("workgroups_graph.json", function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke", function(d) { return color(d.value); });

  var nodes = svg.selectAll(".node")
      .data(graph.nodes)
    .enter()
    .append("g")
      .attr("class", "node")
      .call(force.drag);

  nodes.append("text")
    .attr('x', 6)
    .attr('y', 19)
    .text(function (d) { return d.name; })
    .each(function (d) { d.width = $(this).width(); });

  var nodeRects = nodes.insert("rect", ':first-child')
    .attr("width", function (d) { return d.width + 12; })
    .attr("height",28)
    .attr("rx", 10)
    .attr("ry", 10)
    .style("fill", function(d) { return color(d.group); })
    .call(force.drag);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    nodes.attr("transform", function (d) {
        return "translate(" + (d.x - 25) + "," + (d.y - 10) + ")";
    });
  });
});
