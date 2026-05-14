<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Progetto robotica — Server overview</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous"
    />

    <style>
      body {
        background: #f4f7fb;
        color: #212529;
      }
      .hero {
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #0d6efd10, #0d6efd05);
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
      }
      .card {
        box-shadow: 0 6px 18px rgba(22, 28, 45, 0.06);
      }
      pre.code-snippet {
        background: #0f1720;
        color: #e6eef8;
        padding: 0.75rem;
        border-radius: 0.375rem;
        overflow: auto;
        font-size: 0.9rem;
      }
      .muted-small {
        font-size: 0.9rem;
        color: #6c757d;
      }
      .file-links a {
        display: block;
        color: #0d6efd;
        text-decoration: none;
      }
      @media (max-width: 767px) {
        .hero {
          text-align: center;
        }
      }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container">
        <a class="navbar-brand" href="#">Progetto Robotica</a>
        <div class="d-none d-md-block text-white muted-small">
          Flask server & Dobot code overview
        </div>
      </div>
    </nav>

    <main class="container">
      <div class="hero">
        <div
          class="container d-md-flex justify-content-between align-items-center"
        >
          <div>
            <h1 class="h3 mb-1">Server overview</h1>
            <p class="muted-small mb-0">
              Quick reference for endpoints in <strong>flask_server</strong> and
              robot scripts in <strong>dobot</strong>.
            </p>
          </div>
          <div class="mt-3 mt-md-0 text-md-end">
            <span class="badge bg-light text-dark">Bootstrap</span>
            <span class="badge bg-light text-dark">Vanilla CSS</span>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-lg-7 mb-4">
          <div class="card">
            <div class="card-body">
              <h2 class="h5">Flask Endpoints</h2>
              <p class="muted-small">
                Registered routes and short descriptions (grouped by blueprint).
              </p>

              <div class="list-group">
                <div class="list-group-item">
                  <h5 class="mb-1">Global</h5>
                  <p class="mb-1">
                    <strong>GET /</strong> — Renders this overview page.
                  </p>
                  <p class="mb-1">
                    <strong>GET /status</strong> — Health check: returns
                    <code>{"status":"ok"}</code>.
                  </p>
                </div>

                <div class="list-group-item">
                  <h5 class="mb-1">Blueprint: <code>/robot</code></h5>
                  <ul class="mb-0">
                    <li>
                      <strong>POST /robot/test</strong> — Simple test endpoint:
                      logs received JSON and returns success.
                    </li>
                    <li>
                      <strong>POST /robot/movement_executed</strong> — Receives
                      movement telemetry and forwards it to telemetry link.
                    </li>
                    <li>
                      <strong>POST /robot/infrared_sensor_event</strong> —
                      Infrared sensor events; forwards telemetry.
                    </li>
                    <li>
                      <strong>POST /robot/color_sensor_event</strong> — Color
                      sensor events; forwards telemetry and triggers robot 2.
                    </li>
                  </ul>
                </div>

                <div class="list-group-item">
                  <h5 class="mb-1">Blueprint: <code>/robot1</code></h5>
                  <ul class="mb-0">
                    <li>
                      <strong>GET /robot1/can_collect</strong> — Polled by Robot
                      1 to know if it can collect a block (returns boolean).
                    </li>
                    <li>
                      <strong>POST /robot1/block_dropped</strong> — Called to
                      notify Robot 1 that a block was dropped (sets server
                      flag).
                    </li>
                  </ul>
                </div>

                <div class="list-group-item">
                  <h5 class="mb-1">Blueprint: <code>/robot2</code></h5>
                  <ul class="mb-0">
                    <li>
                      <strong>POST /robot2/block_dropped</strong> — Called by
                      Robot 2 to notify Robot 1 (proxy to robot1).
                    </li>
                    <li>
                      <strong>GET /robot2/detect_color</strong> — Calls Robot 3
                      to detect color, sets internal drop flag.
                    </li>
                    <li>
                      <strong>GET /robot2/can_drop</strong> — Polled by Robot 2
                      to know when it can release a block.
                    </li>
                  </ul>
                </div>

                <div class="list-group-item">
                  <h5 class="mb-1">Blueprint: <code>/robot3</code></h5>
                  <ul class="mb-0">
                    <li>
                      <strong>GET /robot3/detect_color</strong> — Reads camera
                      color via the camera module and returns the detected
                      color.
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-5 mb-4">
          <div class="card">
            <div class="card-body">
              <h2 class="h5">Dobot: Robot scripts</h2>
              <p class="muted-small">
                High-level summary of each robot script in the
                <code>dobot</code> folder.
              </p>

              <div class="mb-3">
                <h6 class="mb-1">robot_1.py</h6>
                <p class="mb-1 muted-small">
                  Robot 1: picks blocks from the collection point and places
                  them on the conveyor. Key features: movement helpers, suction
                  control, polling <code>/robot1/can_collect</code> to wait for
                  permission.
                </p>
                <a
                  class="btn btn-sm btn-outline-primary"
                  data-bs-toggle="collapse"
                  href="#codeRobot1"
                  role="button"
                  aria-expanded="false"
                  aria-controls="codeRobot1"
                  >Show snippet</a
                >
                <div class="collapse mt-2" id="codeRobot1">
                  <pre class="code-snippet">
def main():
  print("[INFO] - Robot 1 started")
  status, code = test_connectivity()
  if not status or code != 200:
    _log("[ERROR] Can't connect to the server")
    return

  # collection_point = Point(-18, -222, 105)
  # conveyor_point = Point(182, -172, 100)
  # main loop: pick, move, drop, wait for server trigger
                  </pre>
                </div>
              </div>

              <div class="mb-3">
                <h6 class="mb-1">robot_2.py</h6>
                <p class="mb-1 muted-small">
                  Robot 2: monitors an infrared sensor, controls conveyor speed,
                  drops blocks and notifies the server. Sends infrared events
                  and movement telemetry.
                </p>
                <a
                  class="btn btn-sm btn-outline-primary"
                  data-bs-toggle="collapse"
                  href="#codeRobot2"
                  role="button"
                  aria-expanded="false"
                  aria-controls="codeRobot2"
                  >Show snippet</a
                >
                <div class="collapse mt-2" id="codeRobot2">
                  <pre class="code-snippet">
def send_ir_event(t = time.time()):
  message = {"ts": str(t), "robot_id": ROBOT_ID, "status": "success"}
  _log(f"[send_ir_event]: {message}")
  requests.post(url=LINK.format("robot/infrared_sensor_event"), json=message)
                  </pre>
                </div>
              </div>

              <div class="mb-3">
                <h6 class="mb-1">robot_3.py</h6>
                <p class="mb-1 muted-small">
                  Robot 3: reads the color sensor and posts detected color to
                  the server (<code>/robot/color_sensor_event</code>).
                </p>
                <a
                  class="btn btn-sm btn-outline-primary"
                  data-bs-toggle="collapse"
                  href="#codeRobot3"
                  role="button"
                  aria-expanded="false"
                  aria-controls="codeRobot3"
                  >Show snippet</a
                >
                <div class="collapse mt-2" id="codeRobot3">
                  <pre class="code-snippet">
def compute_color(values):
  for key, value in values.items():
    if value == 1:
      return key
  return None
                  </pre>
                </div>
              </div>

              <div class="mb-0">
                <h6 class="mb-1">robot_cycle.py</h6>
                <p class="muted-small mb-2">
                  Utility / example cycle script with movement helpers and
                  conveyor controls (variant of robot_2).
                </p>
                <div class="file-links">
                  <a href="/" class="small">Open server root</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-body">
              <h2 class="h6">Reference — important files</h2>
              <p class="muted-small mb-2">
                Quick links to the source files used to generate this overview.
              </p>
              <div class="row">
                <div class="col-sm-6">
                  <ul class="list-unstyled mb-0">
                    <li><a href="/">[server root]</a></li>
                    <li><a href="#">flask_server/main.py</a></li>
                    <li><a href="#">flask_server/blueprints/robot_bp.py</a></li>
                    <li>
                      <a href="#">flask_server/blueprints/robot_1_bp.py</a>
                    </li>
                  </ul>
                </div>
                <div class="col-sm-6">
                  <ul class="list-unstyled mb-0">
                    <li>
                      <a href="#">flask_server/blueprints/robot_2_bp.py</a>
                    </li>
                    <li>
                      <a href="#">flask_server/blueprints/robot_3_bp.py</a>
                    </li>
                    <li><a href="#">dobot/robot_1.py</a></li>
                    <li><a href="#">dobot/robot_2.py</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
      crossorigin="anonymous"
    ></script>
  </body>
</html>
