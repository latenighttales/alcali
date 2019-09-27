const {
  wordBoundaries,
  closestLeftBoundary,
  closestRightBoundary,
  offsetToColRow,
  isIncompleteInput,
  collectAutocompleteCandidates
} = require("./Utils");

/**
 * Test word boundary detection
 */
test("wordBoundaries()", () => {
  expect(wordBoundaries("foo bar baz", true)).toEqual([0, 4, 8]);
  expect(wordBoundaries("foo bar baz", false)).toEqual([3, 7, 11]);
});

/**
 * Test closest left boundary
 */
test("closestLeftBoundary()", () => {
  expect(closestLeftBoundary("foo bar baz", 5)).toEqual(4);
  expect(closestLeftBoundary("foo bar baz", 2)).toEqual(0);
  expect(closestLeftBoundary("foo bar baz", 0)).toEqual(0);
});

/**
 * Test closest right boundary
 */
test("closestRightBoundary()", () => {
  expect(closestRightBoundary("foo bar baz", 5)).toEqual(7);
  expect(closestRightBoundary("foo bar baz", 2)).toEqual(3);
  expect(closestRightBoundary("foo bar baz", 11)).toEqual(11);
});

/**
 * Test offset to row/col de-composition
 */
test("offsetToColRow()", () => {
  const colSize = 25;

  expect(offsetToColRow("test single line case", 0, colSize)).toEqual({
    row: 0,
    col: 0
  });
  expect(offsetToColRow("test single line case", 10, colSize)).toEqual({
    row: 0,
    col: 10
  });
  expect(
    offsetToColRow("test single line case that wraps", 25, colSize)
  ).toEqual({
    row: 0,
    col: 25
  });
  expect(
    offsetToColRow("test single line case that wraps", 26, colSize)
  ).toEqual({
    row: 1,
    col: 0
  });

  expect(offsetToColRow("test\nmulti\nline case\n", 4, colSize)).toEqual({
    row: 0,
    col: 4
  });
  expect(offsetToColRow("test\nmulti\nline case\n", 5, colSize)).toEqual({
    row: 1,
    col: 0
  });
  expect(offsetToColRow("test\nmulti\nline case\n", 6, colSize)).toEqual({
    row: 1,
    col: 1
  });

  expect(
    offsetToColRow(
      "test multiple lines that wraps and\nalso\nnew\nlines",
      25,
      colSize
    )
  ).toEqual({
    row: 0,
    col: 25
  });
  expect(
    offsetToColRow(
      "test multiple lines that wraps and\nalso\nnew\nlines",
      26,
      colSize
    )
  ).toEqual({
    row: 1,
    col: 0
  });
  expect(
    offsetToColRow(
      "test multiple lines that wraps and\nalso\nnew\nlines",
      35,
      colSize
    )
  ).toEqual({
    row: 2,
    col: 0
  });
});

/**
 * Tests if isIncompleteInput correctly detects various cases
 */
test("isIncompleteInput()", () => {
  // Empty input is considered completed
  expect(isIncompleteInput("")).toEqual(false);
  expect(isIncompleteInput("   ")).toEqual(false);

  // Normal cases
  expect(isIncompleteInput("some foo bar")).toEqual(false);
  expect(isIncompleteInput(`some "double quotes"`)).toEqual(false);
  expect(isIncompleteInput(`some 'single quotes'`)).toEqual(false);
  expect(isIncompleteInput(`some 'single "double" quotes'`)).toEqual(false);
  expect(isIncompleteInput(`some && command`)).toEqual(false);

  // Incomplete boolean ops
  expect(isIncompleteInput(`some &&`)).toEqual(true);
  expect(isIncompleteInput(`some &&    `)).toEqual(true);
  expect(isIncompleteInput(`some ||`)).toEqual(true);
  expect(isIncompleteInput(`some ||    `)).toEqual(true);
  expect(isIncompleteInput(`some && foo ||`)).toEqual(true);
  expect(isIncompleteInput(`some && foo || &&`)).toEqual(true);

  // Incomplete pipe
  expect(isIncompleteInput(`some |`)).toEqual(true);
  expect(isIncompleteInput(`some | `)).toEqual(true);

  // Incomplete quote
  expect(isIncompleteInput(`some "command that continues`)).toEqual(true);
  expect(isIncompleteInput(`some "`)).toEqual(true);
  expect(isIncompleteInput(`some "  `)).toEqual(true);
  expect(isIncompleteInput(`some 'same thing with single`)).toEqual(true);
  expect(isIncompleteInput(`some '`)).toEqual(true);
  expect(isIncompleteInput(`some '   `)).toEqual(true);
});

/**
 * Tests if isIncompleteInput correctly detects various cases
 */
test("collectAutocompleteCandidates()", () => {
  const allCb = () => {
    return ["a", "ab", "abc"];
  };

  const firstCb = index => {
    if (index === 1) return ["b", "bc", "bcd"];
    return [];
  };

  const customCb = (index, tokens, custom) => {
    return custom;
  };

  const cbList = [
    { fn: allCb, args: [] },
    { fn: firstCb, args: [] },
    {
      fn: customCb,
      args: [["c", "cd", "cde"]]
    }
  ];

  expect(collectAutocompleteCandidates(cbList, "")).toEqual([
    "a",
    "ab",
    "abc",
    "c",
    "cd",
    "cde"
  ]);
  expect(collectAutocompleteCandidates(cbList, "a")).toEqual([
    "a",
    "ab",
    "abc"
  ]);
  expect(collectAutocompleteCandidates(cbList, "ab")).toEqual([
    "ab",
    "abc"
  ]);

  expect(collectAutocompleteCandidates(cbList, "ab ")).toEqual([
    "a",
    "ab",
    "abc",
    "b",
    "bc",
    "bcd",
    "c",
    "cd",
    "cde"
  ]);
  expect(collectAutocompleteCandidates(cbList, "ab b")).toEqual([
    "b",
    "bc",
    "bcd"
  ]);

});
