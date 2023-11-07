from flask import Flask, render_template, request, redirect, url_for

from pyvis.network import Network
import os
import re

nav_step = 0
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def generate_graph(n):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    net.barnes_hut()
    for i in range(1, n+2):
        net.add_node(i, label=f"Node {i}")
    for i in range(1, n+1):
        net.add_edge(i, i+1)

    neighbor_map = net.get_adj_list()

    for node in net.nodes:
        node["value"] = len(neighbor_map[node["id"]])

    # net.show("templates/network.html", notebook=False)
    html_string = net.generate_html()
    print("html print n: ", n)
    html_string = re.sub('</body>', """ 
        <script type="text/javascript">
        // create a network
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {};
        var network = new vis.Network(container, data, options);

        network.on("click", function(params) {
        if (params.nodes.length > 0) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", '/node', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.send('id=' + params.nodes[0]);
            setTimeout(location.reload.bind(location), 60000)
            document.location.reload();
        }
        });
        </script>
        </body>
        """, html_string)

    with open(os.path.join('templates', 'network.html'), 'w') as f:
        f.write(html_string)

### Initialize graph
generate_graph(7)

@app.route('/')
def home():
    return render_template('network.html')

@app.route('/node', methods=['POST'])
def node():
    node_id = request.form['id']
    ### Update graph and template based on selected node
    generate_graph(int(node_id))
    print(f'Selected node: {node_id}')
    # return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)