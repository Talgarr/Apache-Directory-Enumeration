# Apache-Directory-Enumeration

This python script allow enumeration of Apache "Index Of" pages, such as:

![Index of page](index_of.png)

## Use

```shell
python crawler.py <url> <path> <output_file> <search_type> <max_depth> <--log>
```

Example:

```shell
python crawler.py "http://lms.permx.htb" "/app/" "./apache.json" "BFS" 4
```

Parameters are as follow:

| Parameter     | Type                    | Description                                                  |
| ------------- | ----------------------- | ------------------------------------------------------------ |
| `url`         | String                  | Base url to search.                                          |
| `path`        | String                  | Base path to the apache directory. You need to see the page. |
| `output_file` | String                  | Path to the output file. Should be a `.json`.                |
| `search_type` | String                  | Depth First Search `DFS` or Breath First Search `BFS`.       |
| `max_depth`   | Int                     | The maximum depth the crawler search.                        |
| `--log`       | Optional boolean switch | Activate the printing of logs.                               |

`CTRL + c` Will stop the search and output the current finding.
