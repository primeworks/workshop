<?php

/**
 * @file
 * Hook documentation for the VoguePay WPS module.
 */


/**
 * Allows modules to alter the data array used to create a VoguePay WPS redirect
 * form prior to its form elements being created.
 *
 * @param &$data
 *   The data array used to create redirect form elements.
 * @param $order
 *   The full order object the redirect form is being generated for.
 */
function hook_commerce_voguepay_wps_order_form_data_alter(&$data, $order) {
  // No example.
}
