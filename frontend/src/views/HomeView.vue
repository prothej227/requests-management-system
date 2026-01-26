<template>

  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-1 border-bottom">
    <h1 class="h4 d-flex">
      <i class="bi bi-house me-3"></i>
      Dashboard
    </h1>

    <div class="btn-toolbar mb-2 mb-md-0">
      <button class="btn btn-sm btn-outline-secondary">
        <i class="bi bi-calendar"></i>
        This week
      </button>
    </div>
  </div>

  <!-- KPI Cards -->
  <div class="row g-3 mb-4 mt-1">
    <div class="col-sm-6 col-lg-3">
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between">
            <div>
              <div class="text-muted small">Total Requests</div>
              <div class="fs-4 fw-semibold">128</div>
            </div>
            <i class="bi bi-file-earmark-text fs-3 text-primary"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="col-sm-6 col-lg-3">
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between">
            <div>
              <div class="text-muted small">Pending</div>
              <div class="fs-4 fw-semibold">34</div>
            </div>
            <i class="bi bi-hourglass-split fs-3 text-warning"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="col-sm-6 col-lg-3">
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between">
            <div>
              <div class="text-muted small">Completed</div>
              <div class="fs-4 fw-semibold">82</div>
            </div>
            <i class="bi bi-check-circle fs-3 text-success"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="col-sm-6 col-lg-3">
      <div class="card shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between">
            <div>
              <div class="text-muted small">Cancelled</div>
              <div class="fs-4 fw-semibold">12</div>
            </div>
            <i class="bi bi-x-circle fs-3 text-danger"></i>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Recent Requests Table -->
  <div class="card shadow-sm">
    <div class="card-header d-flex align-items-center justify-content-between">
      <span class="fw-semibold">Recent Requests</span>
      <button class="btn btn-sm btn-outline-primary">
        View all
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Ref No</th>
            <th>Customer</th>
            <th>Category</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>REQ-2026-001</td>
            <td>ABC Corp</td>
            <td>Calibration</td>
            <td>
              <span class="badge bg-warning text-dark">Pending</span>
            </td>
            <td>2026-01-20</td>
          </tr>
          <tr>
            <td>2</td>
            <td>REQ-2026-002</td>
            <td>Delta Industries</td>
            <td>Testing</td>
            <td>
              <span class="badge bg-success">Completed</span>
            </td>
            <td>2026-01-19</td>
          </tr>
          <tr>
            <td>3</td>
            <td>REQ-2026-003</td>
            <td>Nova Labs</td>
            <td>Inspection</td>
            <td>
              <span class="badge bg-warning text-dark">Pending</span>
            </td>
            <td>2026-01-18</td>
          </tr>
          <tr>
            <td>4</td>
            <td>REQ-2026-004</td>
            <td>Zenith Tech</td>
            <td>Calibration</td>
            <td>
              <span class="badge bg-danger">Cancelled</span>
            </td>
            <td>2026-01-17</td>
          </tr>
          <tr>
            <td>5</td>
            <td>REQ-2026-005</td>
            <td>Orion Systems</td>
            <td>Testing</td>
            <td>
              <span class="badge bg-success">Completed</span>
            </td>
            <td>2026-01-16</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  padding-bottom: 2rem;
}
</style>
