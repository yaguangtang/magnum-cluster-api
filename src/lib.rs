use platform_dirs::AppDirs;
use pyo3::prelude::*;
use rand::{distributions::Alphanumeric, Rng};
use slug::slugify;

#[pyfunction]
fn convert_to_rfc1123(input: &str) -> String {
    slugify(input)
}

#[pyfunction]
fn generate_cluster_name() -> String {
    let random_string: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .filter(|c| c.is_ascii_lowercase() || c.is_ascii_digit())
        .take(5)
        .map(char::from)
        .collect();

    format!("kube-{}", random_string)
}

#[pyfunction]
fn user_cache_dir() -> String {
    let app_dirs = AppDirs::new(Some("magnum_cluster_api"), false).unwrap();
    app_dirs.cache_dir.to_str().unwrap().to_string()
}

#[pymodule]
#[pyo3(name = "_internal")]
fn magnum_cluster_api(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_to_rfc1123, m)?)?;
    m.add_function(wrap_pyfunction!(generate_cluster_name, m)?)?;
    m.add_function(wrap_pyfunction!(user_cache_dir, m)?)?;

    Ok(())
}
