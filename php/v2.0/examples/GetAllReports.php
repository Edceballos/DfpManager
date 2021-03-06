<?php
/*
 * Copyright 2015 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Require the base class.
require_once dirname(__DIR__) . "/BaseExample.php";

/**
 * This example gets all reports available to the given user profile. It
 * demonstrates paging through results.
 */
class GetAllReports extends BaseExample {
  /**
   * {@inheritdoc}
   * @see BaseExample::getInputParameters()
   * @return array
   */
  protected function getInputParameters() {
    return array(
        array('name' => 'user_profile_id',
              'display' => 'User Profile ID',
              'required' => true)
    );
  }

  /**
   * {@inheritdoc}
   * @see BaseExample::run()
   */
  public function run() {
    $values = $this->formValues;

    print '<h2>Listing all reports</h2>';

    $reports = null;
    $page_token = null;

    $this->printResultsTableHeader('Reports');
    do {
      $reports = $this->service->reports->listReports(
          $values['user_profile_id'],
          array('pageToken' => $page_token)
      );

      foreach ($reports['items'] as $report) {
        $this->printResultsTableRow($report);
      }

      $page_token = $reports['nextPageToken'];
    } while (!empty($reports['items']) && !empty($page_token));

    $this->printResultsTableFooter();
  }

  /**
   * {@inheritdoc}
   * @see BaseExample::getName()
   * @return string
   */
  public function getName() {
    return 'Get All Reports';
  }

  /**
   * {@inheritdoc}
   * @see BaseExample::getResultsTableHeaders()
   * @return array
   */
  public function getResultsTableHeaders() {
    return array(
        'id' => 'Report ID',
        'name' => 'Report Name',
        'type' => 'Report Type'
    );
  }
}
