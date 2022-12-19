<?php
$lib = new core;
$lib->init($argv);
$lib->run();

class core {
    private $HeaderLine = array(
        0=>"date",
        1=>"paymode",
        2=>"info",
        3=>"payee",
        4=>"wording",
        5=>"amount",
        6=>"category",
        7=>"tags",
    );
    private $input_filename;
    private $output_filename;
    private $bank;
    private $type;

    public function init($args) {
        var_dump($args);

        $this->input_filename = $args[1];
        $this->output_filename = $args[2];
        $this->bank = $args[3];
        $this->type = $args[4];

        //check args
        switch ($this->bank) {
            case "sparkasse":
                //ok
                break;
            case "comdirect":
                //ok
                break;
            case "debug":
                //ok;
                break;
            default:
                //not ok
                throw new Exception("unknown Bank");
                die();
        }
    }

    public function run() {
        $csvData = file_get_contents($this->input_filename);
        $lines = explode(PHP_EOL, $csvData);
        $array = array();
        $fp = fopen($this->output_filename, 'w');
        fputcsv($fp, $this->HeaderLine,";");
        foreach ($lines as $line) {
            $data = str_getcsv($line);
            if ($this->bank == "comdirect") {
                
                if ($this->type == "giro") {
                    $writeLine = array(
                        0=>str_replace(".","/",$data[0]),
                        1=>4,
                        2=>null,
                        3=>null,
                        4=>$data[3],
                        5=>$data[4],
                        6=>null,
                        7=>null,
                    );
                } else if ($this->type == "visa") {
                    $writeLine = array(
                        0=>str_replace(".","/",$data[0]),
                        1=>4,
                        2=>$data[3],
                        3=>null,
                        4=>$data[4],
                        5=>str_replace(",",".",$data[5]),
                        6=>null,
                        7=>null,
                    );
                }
            } else if ($this->bank == "sparkasse") {
                $writeLine = array(
                    0=>str_replace(".","/",$data[1]),
                    1=>4,
                    2=>$data[10],
                    3=>$data[5],
                    4=>$data[4],
                    5=>str_replace(",",".",$data[8]),
                    6=>null,
                    7=>null,
                );
            } else if ($this->bank == "debug") {
                var_dump($data);
                
            } else {
                throw new Exception("NotImplemented?");
            }
            fputcsv($fp, $writeLine,";");
        }
        fclose($fp);
    }
}
